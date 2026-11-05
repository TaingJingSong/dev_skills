# Universal installation — InnoTech agent skills

This guide applies to the standard skill folders in `skills/<name>/SKILL.md`. It does not replace the existing Codex marketplace manifests. The universal installer is the **third-party open-source Skills CLI**, not a custom InnoTech runtime.

## Prerequisites

- Node.js **22.20 or newer** and working `npx`, for the current Skills CLI.
- Git/HTTPS access to the desired repository or an already-extracted local copy.
- Review the source and choose a **trusted, reviewed release**. A skill can include executable scripts; treat it as code, not harmless prompt text.
- Private GitHub repositories require existing authorized Git/SSH/GitHub CLI credentials; do not distribute tokens with skills.

## Easiest installation from the released default branch

```bash
# Interactive: choose target agents and individual skills (project-level by default)
npx skills add taing-jingsong/dev_skills

# All skills for the agents the developer chooses
npx skills add taing-jingsong/dev_skills --skill '*'

# All skills for Claude Code and Cursor, globally for this user
npx skills add taing-jingsong/dev_skills --skill '*' -a claude-code -a cursor -g

# All skills to all agents supported by the CLI, globally (may be excessive)
npx skills add taing-jingsong/dev_skills --all -g
```

**Important:** `owner/repo` resolves the repository default branch; it does not necessarily use `dev`. The commands above become appropriate for v2.1 only after `main` has been promoted and reviewed. Avoid double-installing via both the Codex marketplace and the Skills CLI for the same user/project.

## Test the `dev` branch without releasing it

```bash
git clone --branch dev https://github.com/taing-jingsong/dev_skills.git
npx skills add ./dev_skills --list
npx skills add ./dev_skills
```

The local `./dev_skills` path is interpreted relative to the directory where the command is run. Run from the directory containing the clone (not from inside the clone), or use an absolute path. The CLI scans the canonical `skills/` folder; it does not need a different `SKILL.md` per agent.

## Project vs global scope

- **Project (default):** the current working directory. Run `npx skills add ...` from the target project root, not from the skills source repository, unless you deliberately want to install them there.
- **Global:** add `-g` to make the skills available across repositories for that developer. This does not remotely synchronize cloud agents or make rules persistent in each repository.
- **Selection:** using interactive mode is recommended because installing all skills to every agent can create redundant links or copies.
- **Update:** `npx skills check`, then `npx skills update` (or `npx skills update -g` for global installations).
- **Remove:** `npx skills remove` for an interactive selection; review the exact scope before removal.

The default installation may use symlinks to canonical skill folders. For environments where symlinks do not work, use the CLI's `--copy` flag.

## Protecting existing projects is a separate step

Skills are on-demand instructions. **Installing `project-integrity-guardian` does not automatically make core files read-only.** Each project needs reviewed persistent instruction files plus independent CI / repository permissions for genuine enforcement. If you have a checked-out copy of `dev_skills`, create missing rule files without reinstalling skills:

```bash
cd dev_skills
python -m pip install -r requirements.txt
python scripts/install.py --agent all --scope project --rules-only --project-root /path/to/your-project --dry-run
python scripts/install.py --agent all --scope project --rules-only --project-root /path/to/your-project
```

This creates missing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `.cursor/rules/innotech-guardrails.mdc` from the project template. Existing files are **skipped** and must be reviewed/merged manually. Choose the actual agents instead of `all` when possible. Git-based change guards and CI must run independently of the coding agent to be an effective boundary.

## Compatible agent locations (examples)

| Agent | Common native path | Shared `.agents/skills` support |
|---|---|---|
| OpenAI Codex | `.agents/skills` | Yes |
| Claude Code | `.claude/skills` | Use native path |
| Cursor | `.cursor/skills` | Yes |
| Gemini CLI | `.gemini/skills` | Yes |
| OpenCode | `.opencode/skills` | Yes |
| Roo Code | `.roo/skills` | Yes |
| Cline | `.cline/skills` | Use documented Cline path |
| GitHub Copilot (supported IDEs) | `.github/skills` | Yes in supported clients |

Agent support, global paths, and permission models can change with versions. The Skills CLI is the adapter layer; do not copy identical skills into every native path by hand. Unsupported agents need their own adapter or manual instructions, so **literal "any agent" cannot be guaranteed**.

## Validation

```bash
python scripts/validate_skills.py
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
# After installation, check what the CLI reports:
npx skills list
```

Agent runtime activation is not validated merely by files existing. Verify discovery and activation within each agent your team actually uses.

### References

- Skills CLI: https://github.com/vercel-labs/skills
- Installation reference: https://github.com/vercel-labs/skills/blob/main/docs/commands.md
- Open Agent Skills standard: https://agentskills.io/specification
