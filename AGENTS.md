# Agent Instructions — InnoTech Skills Repository

This repository distributes reusable agent skills and helper scripts. It must remain installable through the existing Codex marketplace and through portable skill directories.

1. Inspect existing conventions and test coverage before editing any skill, script, or plugin metadata.
2. Keep `.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json` compatible. Do not change the marketplace `source.ref` from `main` without explicit release approval.
3. Preserve all existing skill IDs, commands, API behavior, and referenced resources by default. For incompatible changes, document migration requirements and request review.
4. Never add credentials, tokens, sessions, `.env` files, or Git history to distributable releases. Do not execute login, send, or deployment scripts during validation.
5. Treat CI, installer, release builder, guardrails and marketplace manifests as protected. Report any unapproved structural changes instead of making them.
6. For approved work, edit only necessary files, update relevant tests, and run `python scripts/validate_skills.py`, `python scripts/validate_plugin.py`, and `python -m unittest discover -s tests -v`.
7. CI passing is not equivalent to confirming skill discovery in a live agent. State what was and was not tested.
8. Never promote `dev` to `main`, retarget the marketplace, tag a release, or deploy without explicit authorization and human review.

For repository-agnostic rules to install in consumers' projects, see `templates/AGENTS.template.md` and `POLICY.md`.
