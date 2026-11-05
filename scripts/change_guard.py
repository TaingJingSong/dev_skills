#!/usr/bin/env python3
"""Detect edits outside a file allowlist relative to an on-disk snapshot. Not an access sandbox."""
import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

DEFAULT_PROTECTED = ["**/.env", "**/.env.*", "**/credentials.json", "**/token.json", "**/*.pem", "**/*.p12", "**/.git/**"]


def glob_matches(pattern: str, path: str) -> bool:
    """Segment-aware glob: * within a segment; ** spans zero or more segments."""
    if not pattern or pattern.startswith("/") or "\\" in pattern or any(s == ".." for s in pattern.split("/")):
        raise ValueError(f"Invalid policy glob: {pattern!r}")
    pat, parts = tuple(pattern.split("/")), tuple(path.split("/"))

    @lru_cache(None)
    def match(i, j):
        if i == len(pat):
            return j == len(parts)
        if pat[i] == "**":
            return match(i + 1, j) or (j < len(parts) and match(i, j + 1))
        return j < len(parts) and fnmatch.fnmatchcase(parts[j], pat[i]) and match(i + 1, j + 1)

    return match(0, 0)


def git_paths(repo: Path) -> list[str]:
    if not (repo / ".git").exists():
        # Worktrees can have a .git file. Refuse arbitrary directories.
        proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0 or Path(os.fsdecode(proc.stdout).strip()).resolve() != repo.resolve():
            raise ValueError("--repo must be a Git repository root")
    cmd = ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    proc = subprocess.run(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise ValueError("git ls-files failed: " + os.fsdecode(proc.stderr).strip())
    result = []
    for raw in set(proc.stdout.split(b"\0")):
        if not raw:
            continue
        name = os.fsdecode(raw)
        if name.startswith("/") or name.startswith("../") or "/../" in name:
            raise ValueError("Unsafe Git entry")
        result.append(name.replace("\\", "/"))
    return sorted(result)


def snapshot(repo: Path) -> dict:
    state = {}
    for name in git_paths(repo):
        p = repo / name
        if p.is_symlink():
            state[name] = {"type": "symlink", "target": os.readlink(p)}
        elif p.is_file():
            h = hashlib.sha256()
            with p.open("rb") as f:
                for block in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(block)
            state[name] = {"type": "file", "sha256": h.hexdigest(), "executable": bool(p.stat().st_mode & 0o111)}
        elif p.is_dir():
            state[name] = {"type": "directory"}  # e.g. git submodule
        else:
            state[name] = {"type": "missing"}  # tracked deletion
    return {"version": 1, "files": state}


def compare(base: dict, current: dict, policy: dict) -> tuple[list[str], list[str]]:
    allowed = policy.get("allowed_paths")
    extra_protected = policy.get("protected_paths", [])
    if not isinstance(allowed, list) or not allowed or not all(isinstance(x, str) for x in allowed):
        raise ValueError("Policy requires a non-empty allowed_paths string list")
    if not isinstance(extra_protected, list) or not all(isinstance(x, str) for x in extra_protected):
        raise ValueError("protected_paths must be a string list")
    protected = DEFAULT_PROTECTED + extra_protected
    for x in allowed + protected:
        glob_matches(x, "test")
    if base.get("version") != 1 or current.get("version") != 1 or not isinstance(base.get("files"), dict):
        raise ValueError("Invalid baseline format")
    errors, changes = [], []
    old, new = base["files"], current["files"]
    for path in sorted(old.keys() | new.keys()):
        if old.get(path) == new.get(path):
            continue
        op = "ADDED" if path not in old or old.get(path, {}).get("type") == "missing" else "DELETED" if path not in new or new.get(path, {}).get("type") == "missing" else "MODIFIED"
        changes.append(f"{op} {path}")
        if any(glob_matches(x, path) for x in protected):
            errors.append(f"BLOCK protected: {op} {path}")
        elif not any(glob_matches(x, path) for x in allowed):
            errors.append(f"BLOCK outside allowlist: {op} {path}")
        elif op == "DELETED" and not policy.get("allow_deletions", False):
            errors.append(f"BLOCK deletion: {path}")
        elif new.get(path, {}).get("type") == "symlink" and not policy.get("allow_symlinks", False):
            errors.append(f"BLOCK symlink change: {path}")
    return errors, changes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot", help="Record state before authorizing a change")
    snap.add_argument("--repo", type=Path, required=True)
    snap.add_argument("--output", type=Path, required=True, help="Store outside repo and agent write access")
    ver = commands.add_parser("verify", help="Compare current state with an approved baseline/policy")
    ver.add_argument("--repo", type=Path, required=True)
    ver.add_argument("--baseline", type=Path, required=True)
    ver.add_argument("--policy", type=Path, required=True)
    a = p.parse_args()
    try:
        repo = a.repo.resolve(strict=True)
        if a.command == "snapshot":
            out = a.output.resolve()
            if out.is_relative_to(repo):
                raise ValueError("Store baseline outside repo to prevent self-inclusion/tampering")
            if out.exists():
                raise ValueError("Baseline exists; do not overwrite an existing approval baseline")
            data = snapshot(repo)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            print(f"SNAPSHOT {len(data['files'])} Git files -> {out}")
        else:
            data = snapshot(repo)
            baseline = json.loads(a.baseline.read_text(encoding="utf-8"))
            policy = json.loads(a.policy.read_text(encoding="utf-8"))
            errors, changes = compare(baseline, data, policy)
            print(f"CHECKED {len(data['files'])} Git files; {len(changes)} changes")
            for change in changes:
                print("CHANGE", change)
            for error in errors:
                print(error, file=sys.stderr)
            if errors:
                sys.exit(1)
            print("PASS: Changes fit allowlist and protected-path restrictions")
    except (OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
