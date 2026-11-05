# Migration Notes — Original archive to InnoTech Agent Engineering Skills v2

## Preserved and moved

| Original | New path | Status |
|---|---|---|
| `analyze-edge-cases/SKILL.md` | `skills/analyze-edge-cases/SKILL.md` | Preserved + common safety header |
| `generate-test-cases/SKILL.md` | `skills/generate-test-cases/SKILL.md` | Preserved + common safety header |
| `incident-postmortem-generator/SKILL.md` | `skills/incident-postmortem-generator/SKILL.md` | Preserved + common safety header |
| `skills/mobile-core-structure/SKILL.md` (declared `flutter-generate-core-structure`) | `skills/mobile-core-structure/SKILL.md` | Canonical name now `mobile-core-structure`; old invocation may need updating |
| `skills/company-engineering-standard/scripts/telegram_weekly_report/` | `skills/telegram-weekly-report/` | Preview functionality retained and made independently discoverable |
| Other `skills/*/SKILL.md`, `agents/openai.yaml`, `evals/`, `references/`, `prompts/`, `checklists/` | Unchanged relative skill locations | Original knowledge and scaffolding baselines retained |

## Added

- `project-integrity-guardian`, `project-context-analyzer`, `change-impact-analyzer`, `minimal-change-enforcer`, `regression-test-guardian`.
- Shared `POLICY.md`, persistent rule template, metadata validator, agent-aware installer, optional Git change guard, sample path policy, and tests.

## Security and operational corrections

- Removed **bundled** `credentials.json`, `.git/`, macOS metadata and any session/token material from the new distributable ZIP. **If real OAuth credentials were ever pushed or shared, consider revoking/rotating them and checking Git history**; excluding files from this ZIP does not erase history.
- Fixed original `.gitignore` entries that hid several legitimate skill directories from version control. New `.gitignore` protects credential/session artifacts without excluding skills.
- Removed Telegram `login.py` and `send_weekly_report.py` from the new distribution: those scripts contradicted the original skill's explicit no-login/no-send policy. The new `generate_weekly_report_preview.py` takes `--input` and `--output` paths, uses no network/auth and no private defaults.
- Refreshed document helper instructions: `generate_docx.py` is an executor requiring `--script`, not an AI generator. It now exits nonzero (3) on validation failure rather than printing a warning followed by SUCCESS. Approved template `.docx` binaries are not in the original archive.
- Moved optional Google OAuth storage out of the repository by default (`~/.config/innotech/google/`), with environment-variable overrides. OAuth still requires an explicitly authorized user action.
- Split optional Google API requirements from base metadata-tool requirements; removed unneeded `telethon` and `mcp` requirements from the distribution.
- Normalized all discoverable skill names, descriptions and frontmatter. The optional `agents/openai.yaml` files remain product-specific metadata.

## Behavior and compatibility caveats

- Framework skill examples from the original archive are tailored to a particular FastAPI/Nuxt/Flutter design. They are retained as **optional greenfield baselines**, not imposed on arbitrary projects.
- Existing detailed handoff and concise handoff skills are **not merged**, because they serve different outputs.
- `--agent all` makes two copies so both Claude and agents using the shared path can discover skills. Cursor can see both and may surface duplicates; use a single shared installation when possible.
- Existing project instruction files are never overwritten. Merge the rule template manually if your project already has `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
- Agent Skills do not constitute access control or automatic enforcement. For stronger guarantees, use the guard in a trusted CI job, path ownership, PR review, repository permissions and independent tests.
- Tests validate the package tools and metadata, not live Claude/Codex/Gemini/Cursor execution or production behavior of the original framework-specific scripts.


## Marketplace and CI integration (v2.0.0)

- Restored the established `.agents/plugins/marketplace.json` from the original archived `origin/main` and preserved the marketplace name, plugin ID, GitHub URL and `source.ref: main`. Updated display metadata.
- Restored `.codex-plugin/plugin.json` with the same `name` and `skills: ./skills/` entrypoint. Updated description, capabilities and version to `2.0.0`; this change becomes active only after a reviewed `main` release.
- Added `.github/workflows/validate-skills.yml`, `.github/CODEOWNERS`, `AGENTS.md`, `scripts/validate_plugin.py`, `scripts/build_release.py`, `scripts/validate_release.py`, `tests/test_marketplace_release.py`, and `RELEASE_CHECKLIST.md`.
- This distribution is prepared from the previous local v2 source and archived original Git metadata; live `dev` state could not be fetched. Review and resolve any divergence before applying.
