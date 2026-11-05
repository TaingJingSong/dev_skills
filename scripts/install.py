#!/usr/bin/env python3
"""Install the package's skills in native/shared agent directories without clobbering existing skills."""
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from validate_skills import validate

AGENTS = ("codex", "gemini", "cursor", "claude", "shared", "all")


def destinations(agent: str, scope: str, project: Path, home: Path) -> list[Path]:
    base = home if scope == "user" else project
    native = {"codex": base / (".agents/skills"), "gemini": base / (".agents/skills"), "cursor": base / (".agents/skills"), "shared": base / (".agents/skills"), "claude": base / (".claude/skills")}
    if agent == "all":
        return [native["shared"], native["claude"]]
    return [native[agent]]


def rule_destinations(agent: str, scope: str, project: Path) -> list[Path]:
    if scope != "project":
        return []
    choices = {
        "codex": [project / "AGENTS.md"],
        "gemini": [project / "GEMINI.md"],
        "cursor": [project / ".cursor/rules/innotech-guardrails.mdc"],
        "claude": [project / "CLAUDE.md"],
        "shared": [project / "AGENTS.md"],
        "all": [project / "AGENTS.md", project / "GEMINI.md", project / "CLAUDE.md", project / ".cursor/rules/innotech-guardrails.mdc"],
    }
    return choices[agent]


def install(root: Path, agent: str, scope: str, project: Path, home: Path, selected: list[str], force: bool, dry_run: bool, rules: bool, rules_only: bool = False) -> tuple[int, int]:
    problems, count = validate(root)
    if problems:
        raise ValueError("Invalid package: " + "; ".join(problems))
    all_names = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    names = sorted(all_names if not selected else set(selected))
    unknown = set(names) - all_names
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(sorted(unknown)))
    installed = skipped = 0
    backup_root = home / ".innotech-skill-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if not rules_only:
        for dest in destinations(agent, scope, project, home):
            for name in names:
                source = root / "skills" / name
                target = dest / name
                if target.exists() and not force:
                    print(f"SKIP (exists): {target} (add --force to back up and replace)")
                    skipped += 1
                    continue
                if dry_run:
                    print(f"PLAN: {source} -> {target}" + (" (back up existing)" if target.exists() else ""))
                    installed += 1
                    continue
                if target.exists():
                    backup = backup_root / dest.name / dest.parent.name / name
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    if backup.exists():
                        raise ValueError(f"Backup path collision: {backup}")
                    shutil.copytree(target, backup)
                    shutil.rmtree(target)
                    print(f"BACKUP: {backup}")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target)
                print(f"INSTALLED: {target}")
                installed += 1
    if rules or rules_only:
        if scope != "project":
            print("NOTE: --rules only writes project-level instructions, not user/global instructions")
        else:
            data = (root / "templates/AGENTS.template.md").read_text(encoding="utf-8")
            for target in rule_destinations(agent, scope, project):
                if target.exists():
                    print(f"SKIP (existing rules; merge manually): {target}")
                    skipped += 1
                    continue
                text = data
                if target.suffix == ".mdc":
                    text = "---\ndescription: InnoTech project-wide engineering guardrails\nalwaysApply: true\n---\n\n" + data
                if dry_run:
                    print(f"PLAN RULES: {target}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(text, encoding="utf-8")
                    print(f"CREATED RULES: {target}")
                installed += 1
    return installed, skipped


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--agent", choices=AGENTS, default="shared")
    p.add_argument("--scope", choices=("project", "user"), default="project")
    p.add_argument("--project-root", type=Path, default=Path.cwd())
    p.add_argument("--skills", default="", help="Comma-separated skill names; defaults to all")
    p.add_argument("--force", action="store_true", help="Back up and replace existing skill folders")
    p.add_argument("--rules", action="store_true", help="Create project rules when files do not already exist")
    p.add_argument("--rules-only", action="store_true", help="Create project rules without installing skills (for use after npx skills add)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1], help="Package root")
    a = p.parse_args()
    names = [x.strip() for x in a.skills.split(",") if x.strip()]
    try:
        installed, skipped = install(a.source.resolve(), a.agent, a.scope, a.project_root.resolve(), Path.home(), names, a.force, a.dry_run, a.rules, a.rules_only)
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    print(f"Done: {installed} planned/installed, {skipped} skipped. Skill discovery may require agent reload/restart.")


if __name__ == "__main__":
    main()
