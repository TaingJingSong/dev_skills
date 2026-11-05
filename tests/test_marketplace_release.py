"""Offline regression tests for marketplace integration, CI metadata and release packaging."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plugin = load('validate_plugin')
release = load('build_release')
check_release = load('validate_release')


class MarketplaceMetadataTests(unittest.TestCase):
    def test_live_package_manifests_consistent(self):
        self.assertEqual(plugin.check(ROOT), [])

    def test_new_github_owner_is_consistent(self):
        market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        plugin_data = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(market['plugins'][0]['source']['url'], 'https://github.com/taing-jingsong/dev_skills')
        self.assertEqual(plugin_data['interface']['websiteURL'], 'https://github.com/taing-jingsong/dev_skills')
        for rel in ['README.md', 'UNIVERSAL_INSTALL.md', '.github/CODEOWNERS', 'scripts/validate_plugin.py']:
            self.assertNotIn('TaingJingSong', (ROOT / rel).read_text(), rel)

    def test_registered_skill_count(self):
        plugin_data = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(plugin_data['skills'], './skills/')
        self.assertEqual(len(list((ROOT / 'skills').glob('*/SKILL.md'))), 16)

    def test_marketplace_never_points_to_dev(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / '.agents/plugins').mkdir(parents=True)
            (r / '.codex-plugin').mkdir()
            (r / 'skills/a').mkdir(parents=True)
            (r / 'skills/a/SKILL.md').write_text('placeholder')
            (r / '.codex-plugin/plugin.json').write_bytes((ROOT / '.codex-plugin/plugin.json').read_bytes())
            market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
            market['plugins'][0]['source']['ref'] = 'dev'
            (r / '.agents/plugins/marketplace.json').write_text(json.dumps(market))
            self.assertTrue(any('main' in e for e in plugin.check(r)))

    def test_plugin_path_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / '.agents/plugins').mkdir(parents=True)
            (r / '.codex-plugin').mkdir()
            (r / 'skills/a').mkdir(parents=True)
            (r / 'skills/a/SKILL.md').write_text('placeholder')
            (r / '.agents/plugins/marketplace.json').write_bytes((ROOT / '.agents/plugins/marketplace.json').read_bytes())
            data = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
            data['skills'] = '../skills/'
            (r / '.codex-plugin/plugin.json').write_text(json.dumps(data))
            self.assertTrue(any('skills/' in e for e in plugin.check(r)))


class ReleaseTests(unittest.TestCase):
    def test_build_and_validate_zip(self):
        with tempfile.TemporaryDirectory() as d:
            archive = Path(d) / 'release.zip'
            count = release.build(ROOT, archive)
            self.assertGreater(count, 30)
            self.assertEqual(check_release.validate(archive), [])
            with ZipFile(archive) as z:
                self.assertIn('.agents/plugins/marketplace.json', z.namelist())
                self.assertIn('.codex-plugin/plugin.json', z.namelist())
                self.assertIn('UNIVERSAL_INSTALL.md', z.namelist())
                self.assertFalse(any('/.git/' in x for x in z.namelist()))

    def test_releases_are_reproducible(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / 'a.zip', Path(d) / 'b.zip'
            release.build(ROOT, a)
            release.build(ROOT, b)
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_builder_refuses_nested_credential(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / 'skills/sensitive').mkdir(parents=True)
            (r / 'skills/sensitive/credentials.json').write_text('dummy - test only')
            with self.assertRaisesRegex(ValueError, 'Forbidden'):
                release.build(r, r / 'out.zip')

    def test_zip_validator_detects_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            from zipfile import ZIP_DEFLATED
            archive = Path(d) / 'unsafe.zip'
            with ZipFile(archive, 'w', compression=ZIP_DEFLATED) as z:
                z.writestr('../escape.txt', 'unsafe')
            self.assertTrue(any('Unsafe archive' in x for x in check_release.validate(archive)))


if __name__ == '__main__':
    unittest.main()
