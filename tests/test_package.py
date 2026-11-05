import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    p = ROOT / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validate = load("validate_skills")
guard = load("change_guard")
# Importing install.py uses the installed script directory for its sibling import.
sys.path.insert(0, str(ROOT / "scripts"))
installer = load("install")


class MetadataTests(unittest.TestCase):
    def test_all_skills_valid(self):
        problems, total = validate.validate(ROOT)
        self.assertEqual(problems, [])
        self.assertEqual(total, 16)

    def test_original_skills_preserved(self):
        names = {x.parent.name for x in (ROOT / "skills").glob("*/SKILL.md")}
        expected = {"analyze-edge-cases", "generate-test-cases", "incident-postmortem-generator", "capture-implemented-feature", "get-implemented-feature", "generate-implementation-prompt", "company-engineering-standard", "fastapi-generate-core-structure", "frontend-generate-core-structure", "mobile-core-structure", "telegram-weekly-report"}
        self.assertTrue(expected.issubset(names))

    def test_no_secrets_or_git_history_packaged(self):
        for p in ROOT.rglob("*"):
            self.assertNotIn(p.name, ("credentials.json", "token.json", ".git", ".DS_Store", "send_weekly_report.py", "login.py"))
            self.assertFalse(p.name.endswith(".session"))

    def test_descriptions_short_for_cross_agent(self):
        import yaml
        for p in (ROOT / "skills").glob("*/SKILL.md"):
            content = p.read_text()
            desc = yaml.safe_load(content.split("---", 2)[1])["description"]
            self.assertLessEqual(len(desc), 200, p.parent.name)

    def test_frontmatter_name_must_match_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "skills" / "another-skill"
            copy.mkdir(parents=True)
            (copy / "SKILL.md").write_text("---\nname: wrong-name\ndescription: test\n---\n\nInstructions\n")
            problems, _ = validate.validate(Path(temp))
            self.assertTrue(any("name must match" in p for p in problems), problems)

    def test_invalid_nested_skill_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "skills" / "normal"
            copy.mkdir(parents=True)
            (copy / "SKILL.md").write_text("---\nname: normal\ndescription: Test\n---\n\nInstructions\n")
            inner = copy / "scripts" / "SKILL.md"
            inner.parent.mkdir()
            inner.write_text("# Missing frontmatter")
            problems, _ = validate.validate(Path(temp))
            self.assertTrue(any("Noncanonical" in p for p in problems), problems)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()

    def invoke(self, agent="shared", scope="project", names=None, force=False, dry_run=False, rules=False):
        return installer.install(ROOT, agent, scope, self.project, self.home, names or [], force, dry_run, rules)

    def test_shared_project_install(self):
        self.assertEqual(self.invoke(rules=True), (17, 0))
        self.assertTrue((self.project / ".agents/skills/project-integrity-guardian/SKILL.md").exists())
        self.assertTrue((self.project / "AGENTS.md").exists())

    def test_claude_project_install(self):
        self.assertEqual(self.invoke(agent="claude", names=["analyze-edge-cases"], rules=True), (2, 0))
        self.assertTrue((self.project / ".claude/skills/analyze-edge-cases/SKILL.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").exists())

    def test_all_installs_both_paths_and_rules(self):
        self.assertEqual(self.invoke(agent="all", names=["regression-test-guardian"], rules=True), (6, 0))
        self.assertTrue((self.project / ".agents/skills/regression-test-guardian/SKILL.md").exists())
        self.assertTrue((self.project / ".claude/skills/regression-test-guardian/SKILL.md").exists())
        self.assertIn("alwaysApply: true", (self.project / ".cursor/rules/innotech-guardrails.mdc").read_text())

    def test_skips_existing_without_force(self):
        self.invoke(names=["analyze-edge-cases"])
        p = self.project / ".agents/skills/analyze-edge-cases/SKILL.md"
        p.write_text("my custom version")
        self.assertEqual(self.invoke(names=["analyze-edge-cases"]), (0, 1))
        self.assertEqual(p.read_text(), "my custom version")

    def test_force_backups_existing(self):
        self.invoke(names=["analyze-edge-cases"])
        p = self.project / ".agents/skills/analyze-edge-cases/SKILL.md"
        p.write_text("my custom version")
        self.assertEqual(self.invoke(names=["analyze-edge-cases"], force=True), (1, 0))
        self.assertNotEqual(p.read_text(), "my custom version")
        backups = list(self.home.glob(".innotech-skill-backups/**/analyze-edge-cases/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "my custom version")

    def test_dry_run_does_not_write(self):
        self.assertEqual(self.invoke(names=["analyze-edge-cases"], rules=True, dry_run=True), (2, 0))
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_existing_rules_not_overwritten(self):
        rules = self.project / "AGENTS.md"
        rules.write_text("original")
        self.assertEqual(self.invoke(names=["analyze-edge-cases"], rules=True), (1, 1))
        self.assertEqual(rules.read_text(), "original")

    def test_user_scope_writes_no_project_rules(self):
        self.assertEqual(self.invoke(agent="claude", scope="user", names=["analyze-edge-cases"], rules=True), (1, 0))
        self.assertTrue((self.home / ".claude/skills/analyze-edge-cases/SKILL.md").exists())
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_unknown_skill_fails(self):
        with self.assertRaisesRegex(ValueError, "Unknown skills"):
            self.invoke(names=["not-a-real-skill"])


class ChangeGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.put("api/core/main.py", "core")
        self.put("api/features/invoice/a.py", "feature")
        self.put("tests/features/invoice/a_test.py", "test")
        self.base = guard.snapshot(self.repo)
        self.policy = {"allowed_paths": ["api/features/invoice/**", "tests/features/invoice/**"], "protected_paths": ["api/core/**"]}

    def put(self, path, text):
        p = self.repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def check(self):
        return guard.compare(self.base, guard.snapshot(self.repo), self.policy)

    def test_glob_matching(self):
        self.assertTrue(guard.glob_matches("**/core/**", "core/a.py"))
        self.assertTrue(guard.glob_matches("**/core/**", "api/core/a.py"))
        self.assertTrue(guard.glob_matches("api/features/**", "api/features/a/nested.py"))
        self.assertFalse(guard.glob_matches("api/features/*", "api/features/a/nested.py"))
        self.assertFalse(guard.glob_matches("api/core/**", "api/cores/a.py"))

    def test_allowed_edit_and_addition(self):
        self.put("api/features/invoice/a.py", "changed")
        self.put("api/features/invoice/new.py", "new")
        self.assertEqual(self.check()[0], [])

    def test_protected_override_allowlist(self):
        self.policy["allowed_paths"].append("api/core/**")
        self.put("api/core/main.py", "tampered")
        self.assertTrue(any("protected" in x for x in self.check()[0]))

    def test_out_of_scope_blocked(self):
        self.put("api/other/new.py", "new")
        self.assertTrue(any("outside allowlist" in x for x in self.check()[0]))

    def test_default_secret_file_protected(self):
        self.policy["allowed_paths"].append("**")
        self.put(".env", "KEY=x")
        self.assertTrue(any("protected" in x for x in self.check()[0]))

    def test_deletion_rejected(self):
        (self.repo / "api/features/invoice/a.py").unlink()
        self.assertTrue(any("deletion" in x for x in self.check()[0]))

    def test_deletion_explicit_allow(self):
        self.policy["allow_deletions"] = True
        (self.repo / "api/features/invoice/a.py").unlink()
        self.assertEqual(self.check()[0], [])

    def test_symlink_rejected(self):
        (self.repo / "api/features/invoice/link.py").symlink_to("a.py")
        self.assertTrue(any("symlink" in x for x in self.check()[0]))

    def test_baseline_captures_preexisting_dirty_files(self):
        self.assertEqual(self.check()[0], [])
        self.assertIn("api/features/invoice/a.py", self.base["files"])

    def test_policy_globs_reject_traversal(self):
        self.policy["allowed_paths"] = ["../anything"]
        with self.assertRaises(ValueError):
            self.check()

    def test_gitignore_ignored_not_observed(self):
        self.put(".gitignore", "*.cache\n")
        self.base = guard.snapshot(self.repo)
        self.put("invisible.cache", "not tracked")
        self.assertEqual(self.check()[0], [])


class PreviewTests(unittest.TestCase):
    def test_weekly_report_preview_no_network(self):
        script = ROOT / "skills/telegram-weekly-report/scripts/generate_weekly_report_preview.py"
        sample = ROOT / "skills/telegram-weekly-report/assets_report_input_example.json"
        with tempfile.TemporaryDirectory() as temp:
            proc = subprocess.run([sys.executable, str(script), "--input", str(sample), "--output", temp], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("NOT SENT", proc.stdout)
            self.assertEqual(len(list(Path(temp).glob("*.txt"))), 1)
            self.assertEqual(len(list(Path(temp).glob("*.md"))), 1)

    def test_weekly_report_missing_fact_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp) / "in.json"
            input_path.write_text(json.dumps({"week_label": "W1"}))
            script = ROOT / "skills/telegram-weekly-report/scripts/generate_weekly_report_preview.py"
            proc = subprocess.run([sys.executable, str(script), "--input", str(input_path), "--output", temp], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("recipient_display", proc.stderr)


if __name__ == "__main__":
    unittest.main()
