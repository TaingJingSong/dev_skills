# InnoTech Agent Engineering Skills — v2.1.1 (universal-installation ready)

A **cross-agent, cross-language** collection of reusable engineering workflows. This bundle retains your FastAPI, Nuxt, Flutter, QA, postmortem, implementation prompting, documentation and handoff skills, adds five engineering guardrails, and consolidates all discoverable `SKILL.md` files under `skills/<name>/SKILL.md`.

The package follows the [Agent Skills format](https://agentskills.io/specification). It does **not** install model/provider extensions automatically, guarantee skill invocation, or grant enforcement privileges. Agent instructions are guidance; use approved file permissions, CI and code review for enforceable restrictions.

## Directory layout

```text
dev_skills/
├── .agents/plugins/marketplace.json   # Existing Codex marketplace registration; ref=main
├── .codex-plugin/plugin.json       # Existing Codex plugin entrypoint; skills=./skills/
├── .github/workflows/validate-skills.yml
├── .github/CODEOWNERS
├── AGENTS.md                        # Repo-specific rules for contributors and agents
├── skills/
│   ├── project-integrity-guardian/     # New: protected core and structure
│   ├── project-context-analyzer/       # New: read-only architecture discovery
│   ├── change-impact-analyzer/         # New: read-only blast-radius analysis
│   ├── minimal-change-enforcer/        # New: scoped implementations
│   ├── regression-test-guardian/       # New: focused + regression testing
│   ├── analyze-edge-cases/
│   ├── generate-test-cases/
│   ├── incident-postmortem-generator/
│   ├── capture-implemented-feature/
│   ├── get-implemented-feature/
│   ├── generate-implementation-prompt/
│   ├── company-engineering-standard/
│   ├── fastapi-generate-core-structure/
│   ├── frontend-generate-core-structure/
│   ├── mobile-core-structure/
│   └── telegram-weekly-report/
├── scripts/
│   ├── install.py
│   ├── validate_skills.py
│   └── change_guard.py
├── templates/
│   ├── AGENTS.template.md
│   └── change-policy.example.json
├── tests/
├── POLICY.md
├── MIGRATION.md
├── requirements.txt
└── requirements-google.txt
```

## Fastest installation: any supported coding agent

Use the open-source **Skills CLI** to install standard `SKILL.md` skills. **Node.js >=22.20** is needed for current CLI releases. Detailed and safe commands (including `dev` and global installs) are in [UNIVERSAL_INSTALL.md](UNIVERSAL_INSTALL.md).

```bash
# Once this version is released on the repository's main branch:
npx skills add taing-jingsong/dev_skills

# Global install, all skills, all supported agents (can create unnecessary copies):
npx skills add taing-jingsong/dev_skills --all -g
```

The CLI supports interactive agent selection, skill selection, updates and removal. The default is **project-scoped**, whereas `-g` is user/global. It only installs **skills**, not persistent repo instructions or agent toolchains. To initialize repo rules without duplicating already-installed skills, use `python scripts/install.py --agent all --scope project --rules-only --project-root /path/to/project` from a checked-out copy of this repository. Existing rules are never overwritten automatically.

**Prefer a reviewed release/tag for team-wide use.** The public `owner/repo` shorthand resolves the default branch, not `dev`; until v2.1 is released, install locally from `git clone --branch dev ...` and `npx skills add ./dev_skills`. The exact live GitHub branch content is not guaranteed by this local package.

## Release channels: Codex marketplace and portable skills

This repository supports **three installation methods**:

- **Codex marketplace (stable/main):** The preserved `.agents/plugins/marketplace.json` points to `https://github.com/taing-jingsong/dev_skills` at `main`; `.codex-plugin/plugin.json` registers all canonical skills from `./skills/`. Keep the existing command: `codex plugin marketplace add taing-jingsong/dev_skills`, then follow your Codex client’s plugin install/enable flow. The exact marketplace UI and CLI may depend on your Codex version.
- **Universal Skills CLI (recommended):** `npx skills add taing-jingsong/dev_skills`, then select the skills and agents.
- **Portable Python fallback (dev or main):** Clone the selected branch and run `python scripts/install.py` as described below. This is the recommended way to test `dev` without releasing it through the marketplace.

**Promotion rule:** Changes land on `dev` through a reviewed PR, pass CI and an agent smoke test, and are merged to `main` only after explicit release approval. Do not change the marketplace reference from `main` to `dev` during development. GitHub branch protection must be configured by a repo administrator: CI and CODEOWNERS alone do not require reviews.

### Codex marketplace (stable branch)

```bash
codex plugin marketplace add taing-jingsong/dev_skills
# Use your Codex version's plugin UI/commands to enable innotech-dev-plugin.
```

### Test development skills without touching main

```bash
git clone --branch dev https://github.com/taing-jingsong/dev_skills.git
cd dev_skills
python -m pip install -r requirements.txt
python scripts/validate_skills.py
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
python scripts/install.py --agent shared --scope project --project-root /path/to/test-project --dry-run --rules
```

## Python fallback installation

Requires Python 3.10+ for helper scripts (the skill Markdown itself has no runtime dependency). Run commands from the **extracted package root**.

```bash
python -m pip install -r requirements.txt  # only for validator/installer
python scripts/validate_skills.py
```

Recommended single shared installation for **Codex, Gemini CLI and Cursor**:

```bash
python scripts/install.py --agent shared --scope project --project-root /path/to/your-repo --rules
```

For **Claude Code**:

```bash
python scripts/install.py --agent claude --scope project --project-root /path/to/your-repo --rules
```

For teams using all four agents in one repository:

```bash
python scripts/install.py --agent all --scope project --project-root /path/to/your-repo --rules
```

`all` installs both native/shared skill copies. A compatible agent (notably Cursor) can discover both and may display duplicate names. Prefer installing only the agent paths needed, or use a reviewed symlink strategy where supported.

User-wide setup, without writing project policies:

```bash
python scripts/install.py --agent shared --scope user
python scripts/install.py --agent claude --scope user
```

Useful flags:

- `--dry-run`: preview copies without writing.
- `--skills project-integrity-guardian,project-context-analyzer`: install only selected skills.
- `--force`: back up an existing skill directory to `~/.innotech-skill-backups/` and replace it. Without `--force`, existing skills are skipped.
- `--rules-only`: create persistent project instructions **without copying skills**; recommended after universal Skills CLI installation.
- `--rules`: create persistent project instructions only when their target file **does not already exist**. Existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and Cursor rule files are not overwritten; merge manually.

### Agent-specific discovery and persistent instructions

| Agent | Skill directory | Always-on project guidance |
|---|---|---|
| OpenAI Codex | `.agents/skills/` | `AGENTS.md` |
| Claude Code | `.claude/skills/` | `CLAUDE.md` |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `GEMINI.md` |
| Cursor | `.agents/skills/` or `.cursor/skills/` | `.cursor/rules/*.mdc` |

Paths above are common current interfaces; verify compatibility with the installed agent version. Restart or reload if needed. The `agents/openai.yaml` files are **optional Codex UI metadata**, not a general skill requirement. All 16 skills use standard YAML `name` and `description`.

## Recommended workflow

1. **Read the project**: `project-context-analyzer` (read-only).
2. **Analyze impact**: `change-impact-analyzer` when the task could affect other components (read-only).
3. **Protect changes**: `project-integrity-guardian` with the persistent repo rules, and a path allowlist when sensitive.
4. **Implement**: `minimal-change-enforcer` plus the domain skill (FastAPI / Nuxt / Flutter or another project-specific skill).
5. **Verify**: `regression-test-guardian`, with `analyze-edge-cases` or `generate-test-cases` as needed.
6. **Handoff**: `get-implemented-feature` for brief summaries or `capture-implemented-feature` for comprehensive implementation detail.

Do not assume a runtime automatically composes skills in this order. Explicitly request the steps or encode the short protection rules in project instructions.

### Routing boundaries

| Request | Primary skill | Do not confuse with |
|---|---|---|
| List QA cases | `generate-test-cases` | `analyze-edge-cases` (find defects) |
| Audit code for bugs | `analyze-edge-cases` | `generate-test-cases` (test plan) |
| Quick backend handoff | `get-implemented-feature` | detailed `capture-implemented-feature` |
| Comprehensive backend handoff | `capture-implemented-feature` | quick `get-implemented-feature` |
| Create implementation **prompt** | `generate-implementation-prompt` | write code with `minimal-change-enforcer` |
| Existing code modifications | `minimal-change-enforcer` + domain skill | `*-core-structure` examples as a license to restructure |
| Incident RCA | `incident-postmortem-generator` | an unsupported assumption about root cause |

The framework `references/baseline.md` files remain **examples for greenfield scaffolding**, never instructions to reorganize an existing repository.

## Optional change guard

This is a **detective** Git file-state checker. It does not inspect business semantics, ignored files, the internal contents of Git submodules, or prevent a malicious agent from changing files before a check. Protect the snapshot and policy outside the agent's write access; ideally run `verify` in trusted CI.

1. Edit `templates/change-policy.example.json` for the exact feature, allowlist and protected paths. Put the approved copy outside the agent's write access.
2. Before agent work, snapshot the approved baseline **outside the repository**:

```bash
python scripts/change_guard.py snapshot --repo /path/to/your-repo --output /secure/baselines/feature-001.json
```

3. After the work:

```bash
python scripts/change_guard.py verify --repo /path/to/your-repo --baseline /secure/baselines/feature-001.json --policy /secure/policies/feature-001.json
```

It blocks changes outside `allowed_paths`, protected files even when also allowlisted, deletions by default, and new/edited symlinks by default. Wildcards are path-segment-aware (`*` matches within one segment, `**` across segments). For added files under an allowed feature subtree, no existing core edit is needed. For modifications to protected core, **stop and request explicit reviewed approval** rather than editing the policy yourself.

## Optional document and Telegram utilities

- `company-engineering-standard`: retains references, prompts, checklists and document helpers. A `.docx` still requires an authored Node.js generator passed via `--script`; the package is **not** a ready-to-run autonomous DOCX generator and does **not** contain approved binary templates. Install `docx` locally in the JS generator project when required. For optional Google Docs API support, read the helper README and install `requirements-google.txt`; **no credentials are bundled**.
- `telegram-weekly-report`: use `python skills/telegram-weekly-report/scripts/generate_weekly_report_preview.py --input /path/to/report.json --output /path/to/output`. It performs local preview only. No auto-send/login scripts are distributed.

## Validate and test

```bash
python scripts/validate_skills.py
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
python scripts/build_release.py --output /tmp/innotech-agent-skills.zip
python scripts/validate_release.py /tmp/innotech-agent-skills.zip
```

The unit tests are package behavior smoke tests; they do not simulate every coding agent, every repository/framework, or a production deployment. See `MIGRATION.md` for exact changes, intentional exclusions and installation cautions.

## CI, ownership and release procedure

Every push and PR to `dev` or `main` runs `.github/workflows/validate-skills.yml`: validates all 16 skill manifests, checks the marketplace link and entrypoint, runs offline unit tests on Python 3.10 and 3.12, verifies portable installation paths, and checks the resulting distribution ZIP for known sensitive filenames and traversal paths. This is **not** a real Codex/Claude/Gemini/Cursor runtime execution test.

For safe promotion, configure a GitHub ruleset protecting `main`: require PRs, at least one human approval, Code Owner review, passing `Validate Agent Skills / Python 3.10` and `Validate Agent Skills / Python 3.12` checks, and prevent force pushes. Also protect `dev` using appropriate review and CI requirements. Do **not** grant the coding agent permissions to bypass these rules.

Review `RELEASE_CHECKLIST.md` before merging to `main` or tagging a release. Build a local safe ZIP with `python scripts/build_release.py --output /tmp/innotech-agent-skills.zip` and validate with `python scripts/validate_release.py /tmp/innotech-agent-skills.zip`.

Avoid adding real credentials or `.env` files. If secrets were ever committed, rotate/revoke them and consult a repository administrator about historical cleanup; `.gitignore` and safe ZIPs do not remove past exposure.
