"""Copy selected skills to a client directory without replacing existing skills."""
import argparse
from pathlib import Path
import re
import shutil

REPO = Path(__file__).resolve().parents[1]


def install(target, names=None, source_root=None):
    source_root = Path(source_root or REPO / "skills").resolve()
    available = sorted(p.name for p in source_root.iterdir()
                       if p.is_dir() and not p.is_symlink() and (p / "SKILL.md").is_file())
    names = list(dict.fromkeys(names or available))
    if not names:
        raise ValueError("No skills found")
    for name in names:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name not in available:
            raise ValueError("Unknown or invalid skill name")
        if any(p.is_symlink() for p in (source_root / name).rglob("*")):
            raise ValueError("Symlinks in a source skill are not supported")
    target = Path(target).expanduser().resolve()
    if target == source_root or source_root in target.parents or target in source_root.parents:
        raise ValueError("Installation target must not overlap the source tree")
    conflicts = [name for name in names
                 if (target / name).exists() or (target / name).is_symlink()]
    if conflicts:
        raise FileExistsError("Skill already exists: " + ", ".join(conflicts))
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(source_root / name, target / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--skill", action="append")
    args = parser.parse_args()
    try:
        names = install(args.target, args.skill)
    except (OSError, ValueError) as error:
        print(type(error).__name__ + ": installation stopped; inspect target and skill names")
        return 1
    print("Installed " + str(len(names)) + " skill(s): " + ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
