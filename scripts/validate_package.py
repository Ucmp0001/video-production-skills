"""Check skill structure and local references without requiring extra packages."""
import argparse
import json
from pathlib import Path
import re


def validate(root):
    root = Path(root).resolve()
    errors, names = [], []
    skills = root / "skills"
    if not skills.is_dir():
        return {"skills": [], "errors": ["Missing skills directory"]}
    for folder in sorted(skills.iterdir()):
        if not folder.is_dir():
            continue
        skill = folder / "SKILL.md"
        if not skill.is_file():
            errors.append(f"{folder.name}: missing SKILL.md")
            continue
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        if not match:
            errors.append(f"{folder.name}: invalid frontmatter")
            continue
        fields = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip("\"'")
        name = fields.get("name", "")
        if name != folder.name or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{folder.name}: invalid name")
        if not fields.get("description"):
            errors.append(f"{folder.name}: missing description")
        if len(text.split()) > 1800:
            errors.append(f"{folder.name}: oversized entrypoint; move detail to references")
        names.append(name)
        english = folder / "SKILL.en.md"
        if not english.is_file() or not english.read_text(encoding="utf-8").strip():
            errors.append(f"{folder.name}: missing English instructions")
        if "[SKILL.en.md](SKILL.en.md)" not in text:
            errors.append(f"{folder.name}: missing English routing")
        for reference in (folder / "references").glob("*.md"):
            if reference.name.endswith(".en.md"):
                continue
            translated = reference.with_name(reference.stem + ".en.md")
            if not translated.is_file() or not translated.read_text(encoding="utf-8").strip():
                errors.append(f"{folder.name}: missing English reference {reference.name}")
        ui = folder / "agents" / "openai.yaml"
        if not ui.is_file():
            errors.append(f"{folder.name}: missing UI metadata")
        else:
            values = dict(re.findall(r'^\s+(display_name|short_description|default_prompt): "([^"]+)"\s*$',
                                     ui.read_text(encoding="utf-8"), re.M))
            if len(values) != 3 or "$" + name not in values.get("default_prompt", ""):
                errors.append(f"{folder.name}: invalid UI metadata")
            if not 25 <= len(values.get("short_description", "")) <= 64:
                errors.append(f"{folder.name}: short description length")
    for doc in root.rglob("*.md"):
        if any(p in {".git", "__pycache__"} for p in doc.relative_to(root).parts):
            continue
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+://|^#", link):
                continue
            target = (doc.parent / link.split("#", 1)[0]).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f"{doc.relative_to(root).as_posix()}: invalid local link")
    if len(names) != len(set(names)):
        errors.append("Duplicate skill names")
    return {"skills": names, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    try:
        result = validate(args.root)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"error_type": type(error).__name__}))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
