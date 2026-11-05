#!/usr/bin/env python3
"""Verify archive safety and required plugin files before sharing a release ZIP."""
import argparse
import sys
from pathlib import PurePosixPath
from zipfile import ZipFile, BadZipFile

REQUIRED = {'README.md', 'AGENTS.md', '.agents/plugins/marketplace.json', '.codex-plugin/plugin.json', 'skills/project-integrity-guardian/SKILL.md', 'scripts/validate_plugin.py'}
FORBIDDEN = {'.git', 'credentials.json', 'token.json', '.env', '.DS_Store', '__MACOSX', '__pycache__'}
BAD_EXT = {'.pem', '.p12', '.pfx', '.key', '.session', '.pyc'}


def validate(path) -> list[str]:
    errors = []
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                errors.append('Duplicate archive entries')
            for info in archive.infolist():
                parts = PurePosixPath(info.filename).parts
                if info.filename.startswith('/') or '..' in parts or not parts:
                    errors.append(f'Unsafe archive member: {info.filename}')
                if any(part in FORBIDDEN for part in parts) or any(part.startswith('.env.') for part in parts) or PurePosixPath(info.filename).suffix in BAD_EXT:
                    errors.append(f'Forbidden release member: {info.filename}')
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    errors.append(f'Symlink forbidden in release: {info.filename}')
            missing = REQUIRED - set(names)
            if missing:
                errors.append('Missing required release files: ' + ', '.join(sorted(missing)))
    except (BadZipFile, OSError) as exc:
        errors.append(f'Could not read ZIP: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    args = parser.parse_args()
    errors = validate(args.archive)
    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
    print('PASS: release archive is structurally valid and excludes known sensitive filenames')


if __name__ == '__main__':
    main()
