# InnoTech Agent Engineering Skills — v2

A **cross-agent, cross-language** collection of reusable engineering workflows. This bundle retains your FastAPI, Nuxt, Flutter, QA, postmortem, implementation prompting, documentation and handoff skills, adds five engineering guardrails, and consolidates all discoverable `SKILL.md` files under `skills/<name>/SKILL.md`.

The package follows the [Agent Skills format](https://agentskills.io/specification). It does **not** install model/provider extensions automatically, guarantee skill invocation, or grant enforcement privileges. Agent instructions are guidance; use approved file permissions, CI and code review for enforceable restrictions.

## Directory layout

```text
innotech-plugin-v2/
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

## Installation

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
python -m unittest discover -s tests -v
python -m compileall -q scripts skills
```

The unit tests are package behavior smoke tests; they do not simulate every coding agent, every repository/framework, or a production deployment. See `MIGRATION.md` for exact changes, intentional exclusions and installation cautions.
