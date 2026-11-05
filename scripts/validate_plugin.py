#!/usr/bin/env python3
"""Validate the existing Codex marketplace schema and portable skill registration."""
import argparse
import json
import re
import sys
from pathlib import Path


def check(root: Path) -> list[str]:
    errors = []
    marketplace = root / '.agents/plugins/marketplace.json'
    plugin = root / '.codex-plugin/plugin.json'
    for path in (marketplace, plugin):
        if not path.is_file():
            errors.append(f'Missing required manifest: {path.relative_to(root)}')
    if errors:
        return errors
    try:
        market = json.loads(marketplace.read_text(encoding='utf-8'))
        entry = json.loads(plugin.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        return [f'Invalid JSON: {exc}']
    if not isinstance(market, dict) or not isinstance(entry, dict):
        return ['Marketplace and plugin manifests must both contain JSON objects']
    plugins = market.get('plugins')
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        return ['Marketplace must contain one plugin entry (review new entries explicitly)']
    listing = plugins[0]
    if listing.get('name') != entry.get('name'):
        errors.append('Marketplace plugin name does not match plugin.json')
    source = listing.get('source')
    if not isinstance(source, dict) or source.get('source') != 'url' or source.get('url') != 'https://github.com/taing-jingsong/dev_skills':
        errors.append('Marketplace source repository changed or is invalid')
    if not isinstance(source, dict) or source.get('ref') != 'main':
        errors.append('Marketplace source must remain main until separately approved')
    if not isinstance(entry.get('name'), str) or not entry['name']:
        errors.append('Plugin name missing')
    if not isinstance(entry.get('version'), str) or not re.fullmatch(r'\d+\.\d+\.\d+', entry['version']):
        errors.append('Plugin version must be a semantic version (X.Y.Z)')
    if entry.get('skills') != './skills/':
        errors.append('Plugin skill registration must remain ./skills/')
    skills_dir = root / 'skills'
    if not skills_dir.is_dir() or not list(skills_dir.glob('*/SKILL.md')):
        errors.append('Plugin registered skills directory is missing or empty')
    # Do not allow a mistakenly renamed directory or symlink to escape the package.
    if skills_dir.is_symlink():
        errors.append('Plugin skills directory must not be a symlink')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
    print('PASS: marketplace registration and portable skills path are consistent')


if __name__ == '__main__':
    main()
