#!/usr/bin/env python3
"""Create a deterministic, safe source ZIP without credentials or repository history."""
import argparse
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT_FILES = {'AGENTS.md', 'README.md', 'MIGRATION.md', 'POLICY.md', 'RELEASE_CHECKLIST.md', 'UNIVERSAL_INSTALL.md', '.gitignore', 'requirements.txt', 'requirements-google.txt'}
ROOT_DIRS = {'skills', 'scripts', 'templates', 'tests'}
META_PREFIXES = {'.agents/plugins/', '.codex-plugin/', '.github/workflows/', '.github/CODEOWNERS'}
BAD_NAMES = {'credentials.json', 'token.json', '.DS_Store', '.env', 'id_rsa', 'id_ed25519'}
BAD_EXTENSIONS = {'.pem', '.p12', '.pfx', '.key', '.session', '.pyc'}


def allowed(rel: Path) -> bool:
    name = rel.as_posix()
    if len(rel.parts) == 1 and name in ROOT_FILES:
        return True
    return (rel.parts[0] in ROOT_DIRS and len(rel.parts) > 1) or any(name.startswith(prefix) for prefix in META_PREFIXES)


def files_to_package(root: Path) -> list[Path]:
    selected = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '__MACOSX'} for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f'Symlinks are not allowed in release: {rel}')
        if not path.is_file():
            continue
        if path.name in BAD_NAMES or path.suffix in BAD_EXTENSIONS or path.name.startswith('.env.'):
            raise ValueError(f'Forbidden secret/artifact file: {rel}')
        if allowed(rel):
            selected.append(path)
    return sorted(selected, key=lambda p: p.relative_to(root).as_posix())


def build(root: Path, output: Path) -> int:
    files = files_to_package(root)
    if not files:
        raise ValueError('Nothing to package')
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix('.zip.tmp')
    try:
        with ZipFile(tmp, 'w', compression=ZIP_DEFLATED, compresslevel=9) as z:
            for path in files:
                rel = path.relative_to(root).as_posix()
                info = ZipInfo(rel, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = (0o100644 & 0xffff) << 16
                z.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
        os.replace(tmp, output)
    finally:
        if tmp.exists():
            tmp.unlink()
    return len(files)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    try:
        count = build(args.root.resolve(), args.output.resolve())
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    print(f'PASS: built release ZIP with {count} files: {args.output}')


if __name__ == '__main__':
    main()
