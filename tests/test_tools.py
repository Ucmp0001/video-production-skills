import hashlib
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


srt = load("srt_checker", "skills/voice-subtitle-sync/scripts/check_srt.py")
manifest = load("source_manifest", "skills/video-source-index/scripts/source_manifest.py")
privacy = load("privacy_scanner", "scripts/privacy_scan.py")
installer = load("skill_installer", "scripts/install_skills.py")
validator = load("package_validator", "scripts/validate_package.py")


class SubtitleTests(unittest.TestCase):
    def test_valid_unicode_and_bom(self):
        text = "\ufeff1\r\n00:00:00,000 --> 00:00:02,000\r\n中文字幕\r\n"
        result = srt.check(text, 2)
        self.assertEqual(result["cues"], 1)
        self.assertFalse(result["errors"])
        self.assertFalse(result["warnings"])

    def test_invalid_minute_and_zero_duration(self):
        malformed = srt.check("1\n00:61:00,000 --> 00:62:00,000\nText")
        self.assertEqual(malformed["errors"][0]["code"], "invalid_timestamp")
        zero = srt.check("1\n00:00:01,000 --> 00:00:01,000\nText")
        self.assertIn("nonpositive_duration", [x["code"] for x in zero["errors"]])

    def test_overlap_is_warning_and_media_bounds_are_errors(self):
        result = srt.check("1\n00:00:00,000 --> 00:00:02,000\nOne\n\n"
                           "2\n00:00:01,500 --> 00:00:03,000\nTwo", duration=2.5)
        self.assertIn("overlap", [x["code"] for x in result["warnings"]])
        self.assertIn("exceeds_media", [x["code"] for x in result["errors"]])

    def test_readability_uses_caption_text(self):
        result = srt.check("1\n00:00:00,000 --> 00:00:00,200\n<b>中文测试</b>")
        codes = [x["code"] for x in result["warnings"]]
        self.assertIn("short_hold", codes)
        # Exactly 20 cps; HTML markup must not increase the measured rate.
        self.assertNotIn("reading_speed", codes)

    def test_bad_configuration_and_empty_file(self):
        for value in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                srt.check("test", duration=value)
        self.assertTrue(srt.check("")["errors"])


class ManifestTests(unittest.TestCase):
    def test_hash_no_paths_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, output = root / "clip.bin", root / "manifest.json"
            source.write_bytes(b"source content")
            with patch.object(manifest.shutil, "which", return_value=None):
                data = manifest.write_manifest(source, output)
            entry = data["sources"][0]
            self.assertEqual(entry["sha256"], hashlib.sha256(b"source content").hexdigest())
            self.assertEqual(entry["rights_status"], "unknown")
            self.assertEqual(entry["probe_status"], "unavailable")
            self.assertNotIn(str(root), output.read_text(encoding="utf-8"))
            before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                manifest.write_manifest(source, output)
            self.assertEqual(before, output.read_bytes())

    def test_probe_output_drops_private_tags(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "clip.mp4"
            source.write_bytes(b"fixture")
            fake = type("Result", (), {"stdout": json.dumps({
                "format": {"duration": "1", "tags": {"artist": "Private Artist"}},
                "streams": [{"codec_type": "video", "width": 100, "height": 100,
                             "tags": {"comment": "private"}}]
            }).encode()})()
            with patch.object(manifest.shutil, "which", return_value="ffprobe"), \
                    patch.object(manifest.subprocess, "run", return_value=fake):
                entry = manifest.source_entry(source)
            self.assertEqual(entry["probe_status"], "complete")
            self.assertNotIn("Private Artist", json.dumps(entry))
            self.assertNotIn("tags", json.dumps(entry))


class PrivacyTests(unittest.TestCase):
    def categories(self, text, terms=()):
        result = privacy.inspect_text(text, terms)
        self.assertNotIn(text, json.dumps(result))
        return {x["category"] for x in result}

    def test_known_token_shapes(self):
        samples = [
            "sk" + "-" + "a" * 24,
            "gh" + "p_" + "b" * 30,
            "AK" + "IA" + "Z" * 16,
            "Bearer" + " " + "t" * 24,
            "-----BEGIN " + "PRIVATE KEY-----",
            "eyJ" + "a" * 20 + "." + "b" * 20 + "." + "c" * 20,
        ]
        for sample in samples:
            self.assertTrue(self.categories(sample), "A known credential shape was missed")

    def test_assignment_signed_url_email_and_path(self):
        samples = [
            ("api_key" + '="' + "abc" * 8 + '"', "credential_assignment"),
            ("https://example.invalid/file?" + "signature=" + "abc123", "signed_url"),
            ("https://u:" + "pass123" + "@example.invalid/", "url_credentials"),
            ("reader" + "@" + "example.invalid", "email"),
            ("C:" + "/Users/" + "sample/video.mp4", "personal_path"),
        ]
        for text, category in samples:
            self.assertIn(category, self.categories(text))

    def test_private_terms_are_case_insensitive(self):
        self.assertIn("private_deny_term", self.categories("Sensitive Alias", ["sensitive alias"]))

    def test_hash_is_not_a_secret(self):
        self.assertFalse(privacy.inspect_text(hashlib.sha256(b"public").hexdigest()))

    def test_binary_and_unlisted_private_file_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".env").write_text("ordinary text", encoding="utf-8")
            (root / "clip.mp4").write_bytes(b"\0binary")
            result = privacy.scan(root)
            self.assertIn("private_artifact", {x["category"] for x in result["findings"]})
            self.assertIn("outside_publish_allowlist", {x["category"] for x in result["findings"]})


class InstallTests(unittest.TestCase):
    def test_full_install_preserves_bilingual_instructions_and_references(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "skills"
            installed = installer.install(target)
            self.assertEqual(len(installed), 11)
            for source in (REPO / "skills").iterdir():
                if not source.is_dir():
                    continue
                for relative in [Path("SKILL.md"), Path("SKILL.en.md"),
                                 *[p.relative_to(source) for p in (source / "references").glob("*.md")]]:
                    self.assertEqual((source / relative).read_bytes(),
                                     (target / source.name / relative).read_bytes())

    def test_installed_tools_run_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "installed"
            work = root / "work"
            work.mkdir()
            installer.install(target, ["video-source-index", "voice-subtitle-sync"])
            source = work / "source.bin"
            source.write_bytes(b"synthetic source")
            captions = work / "captions.srt"
            captions.write_text("1\n00:00:00,000 --> 00:00:02,000\nTest\n", encoding="utf-8")
            commands = [
                [sys.executable, str(target / "video-source-index/scripts/source_manifest.py"),
                 str(source), "--output", str(work / "manifest.json")],
                [sys.executable, str(target / "voice-subtitle-sync/scripts/check_srt.py"),
                 str(captions), "--duration", "2"],
            ]
            for command in commands:
                result = subprocess.run(command, cwd=work,
                                        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                                        capture_output=True, timeout=45)
                self.assertEqual(result.returncode, 0)
                json.loads(result.stdout)

    def fixture(self, root):
        source = root / "source"
        for name in ("one-skill", "two-skill"):
            (source / name).mkdir(parents=True)
            (source / name / "SKILL.md").write_text("public skill", encoding="utf-8")
        return source

    def test_install_and_preflight_conflict(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, target = self.fixture(root), root / "target"
            installer.install(target, ["one-skill"], source)
            with self.assertRaises(FileExistsError):
                installer.install(target, ["two-skill", "one-skill"], source)
            self.assertFalse((target / "two-skill").exists())
            self.assertEqual((target / "one-skill" / "SKILL.md").read_text(), "public skill")

    def test_invalid_names_and_overlap(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = self.fixture(root)
            with self.assertRaises(ValueError):
                installer.install(root / "target", ["../escape"], source)
            with self.assertRaises(ValueError):
                installer.install(source / "nested", ["one-skill"], source)

    def test_symlink_source_rejected_when_supported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = self.fixture(root)
            link = source / "one-skill" / "outside.md"
            try:
                link.symlink_to(source / "two-skill" / "SKILL.md")
            except OSError:
                self.skipTest("Host does not allow symlink creation")
            with self.assertRaises(ValueError):
                installer.install(root / "target", ["one-skill"], source)


class PackageTests(unittest.TestCase):
    def test_missing_english_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = root / "skills" / "evidence-story-script"
            shutil.copytree(REPO / "skills" / skill.name, skill)
            (skill / "references" / "story-evidence.en.md").unlink()
            result = validator.validate(root)
            self.assertTrue(any("missing English reference" in e for e in result["errors"]))

    def test_missing_english_entrypoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = root / "skills" / "evidence-story-script"
            shutil.copytree(REPO / "skills" / skill.name, skill)
            (skill / "SKILL.en.md").unlink()
            result = validator.validate(root)
            self.assertTrue(any("missing English instructions" in e for e in result["errors"]))

    def test_all_skills_and_links(self):
        result = validator.validate(REPO)
        self.assertEqual(len(result["skills"]), 11)
        self.assertFalse(result["errors"], result["errors"])

    def test_package_has_no_privacy_findings(self):
        result = privacy.scan(REPO)
        self.assertFalse(result["findings"], result["findings"])


if __name__ == "__main__":
    unittest.main()
