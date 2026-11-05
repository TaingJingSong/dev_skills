#!/usr/bin/env python3
"""Portable static validator for the InnoTech Agent Skills package."""
import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BAD_PARTS = {"__MACOSX", ".DS_Store", "credentials.json", "token.json"}


def validate(root: Path) -> tuple[list[str], int]:
    try:
        import yaml
    except ImportError:
        return ["PyYAML missing: install with `python -m pip install -r requirements.txt`"], 0
    errors = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return ["Missing skills/ directory"], 0
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        return ["No top-level SKILL.md files found"], 0
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts or "node_modules" in rel.parts:
            continue
        if any(part in BAD_PARTS for part in rel.parts) or path.name.endswith((".session", ".pem", ".p12", ".pfx")):
            errors.append(f"Forbidden packaged file: {rel}")
        if path.is_file() and path.name == "SKILL.md" and path not in skill_files:
            errors.append(f"Noncanonical nested skill: {rel}")
    seen = set()
    for path in skill_files:
        name = path.parent.name
        data = path.read_text(encoding="utf-8")
        m = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", data, re.DOTALL)
        if not m:
            errors.append(f"{path.relative_to(root)}: missing first-line YAML frontmatter")
            continue
        try:
            front = yaml.safe_load(m.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"{name}: invalid YAML: {exc}")
            continue
        if not isinstance(front, dict):
            errors.append(f"{name}: YAML must be a mapping")
            continue
        declared = front.get("name")
        desc = front.get("description")
        if not isinstance(declared, str) or declared != name or not NAME_RE.fullmatch(declared) or len(declared) > 64:
            errors.append(f"{name}: name must match directory and use lowercase letters/numbers/hyphens")
        if declared in seen:
            errors.append(f"Duplicate skill: {declared}")
        seen.add(declared)
        if not isinstance(desc, str) or not 1 <= len(desc) <= 1024:
            errors.append(f"{name}: description must be a non-empty string up to 1024 chars")
        compatibility = front.get("compatibility")
        if compatibility is not None and (not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500):
            errors.append(f"{name}: compatibility must be <=500 characters")
        if not data[m.end():].strip():
            errors.append(f"{name}: empty body")
        if name == "telegram-weekly-report" and (path.parent / "scripts/send_weekly_report.py").exists():
            errors.append("Telegram preview skill contains auto-send script")
    return errors, len(skill_files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, count = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {count} agent skills validated; no forbidden package artifacts")


if __name__ == "__main__":
    main()
