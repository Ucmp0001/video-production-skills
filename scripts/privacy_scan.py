"""Heuristic public-package preflight. Reports categories, never matched values."""
import argparse
import json
import math
from pathlib import Path
import re

TOP_FILES = {"README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "CONTRIBUTING.md",
             "SECURITY.md", ".gitignore", "README.en.md", "CONTRIBUTING.en.md",
             "SECURITY.en.md", "THIRD_PARTY_NOTICES.en.md"}
TOP_DIRS = {"skills", "scripts", "tests", "docs", "examples", "licenses", ".github"}
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
SKIP_DIRS = {".git", "__pycache__"}
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "service_token": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|"
                                r"github_pat_[A-Za-z0-9_]{20,}|"
                                r"AKIA[A-Z0-9]{16}|xox[baprs]-[A-Za-z0-9-]{16,})\b"),
    "bearer": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "credential_assignment": re.compile(
        r"""(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|secret[_-]?key)\b["']?\s*[:=]\s*["']([A-Za-z0-9_./+=-]{12,})["']"""),
    "signed_url": re.compile(r"https?://[^\s<>\"']+[?&](?:"
                             r"token|access_token|api_key|key|signature|sig|"
                             r"x-amz-signature|x-goog-signature)=[^&\s<>\"']+", re.I),
    "url_credentials": re.compile(r"https?://[^/\s:@]+:[^/\s@]+@", re.I),
    "personal_path": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|商业)[\\/]|"
                                r"/(?:Users|home)/[A-Za-z0-9_.-]+/)", re.I),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}
ENTROPY_CANDIDATE = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z0-9_+/=-]{32,}(?![A-Za-z0-9_])")


def entropy(value):
    return -sum((value.count(c) / len(value)) * math.log2(value.count(c) / len(value))
                for c in set(value))


def inspect_text(text, deny_terms=()):
    findings = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for category, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append({"line": line_no, "category": category})
        if any(term.casefold() in line.casefold() for term in deny_terms if term):
            findings.append({"line": line_no, "category": "private_deny_term"})
        for match in ENTROPY_CANDIDATE.finditer(line):
            value = match.group()
            if re.fullmatch(r"[a-fA-F0-9]{32,128}", value):
                continue
            if any(c.isupper() for c in value) and any(c.islower() for c in value) and \
                    any(c.isdigit() for c in value) and entropy(value) >= 4.5:
                findings.append({"line": line_no, "category": "high_entropy_candidate"})
                break
    return findings


def scan(root, deny_terms=()):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Package root must be a directory")
    findings, count = [], 0
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            findings.append({"file": rel.as_posix(), "category": "symlink"})
            continue
        if not path.is_file():
            continue
        count += 1
        name = rel.as_posix()
        if (len(rel.parts) == 1 and name not in TOP_FILES) or \
                (len(rel.parts) > 1 and rel.parts[0] not in TOP_DIRS) or \
                (len(rel.parts) > 1 and path.suffix not in EXTENSIONS):
            findings.append({"file": name, "category": "outside_publish_allowlist"})
        if path.name.startswith(".env") or path.suffix.lower() in \
                {".key", ".pem", ".p12", ".pfx", ".log", ".mp4", ".wav", ".zip"}:
            findings.append({"file": name, "category": "private_artifact"})
            continue
        for item in inspect_text(name, deny_terms):
            findings.append({"file": name, "category": item["category"], "line": 0})
        try:
            if path.stat().st_size > 1_000_000:
                findings.append({"file": name, "category": "unexpected_large_file"})
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            findings.append({"file": name, "category": "unreadable_or_binary"})
            continue
        for item in inspect_text(text, deny_terms):
            findings.append({"file": name, **item})
    return {"files_scanned": count, "findings": findings,
            "note": "Heuristic preflight; manual review and commit-metadata checks remain necessary."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--deny-file", type=Path,
                        help="Local-only UTF-8 file containing one private deny term per line")
    args = parser.parse_args()
    try:
        terms = args.deny_file.read_text(encoding="utf-8-sig").splitlines() if args.deny_file else []
        result = scan(args.root, terms)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return int(bool(result["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
