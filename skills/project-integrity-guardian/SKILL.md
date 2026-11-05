---
name: project-integrity-guardian
description: Protect existing architecture, core code, public contracts and repository structure during coding. Use for safe scoped changes and to report protected edits as proposals.
---

# Project Integrity Guardian

## Mission

Prevent unauthorized modifications to established project structure, core services, and public behavior. **Start read-only.** The task scope and repo-specific rules decide what is actually editable; never assume blanket permission.

## Pre-change checklist

1. Inspect repository policy (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, relevant nested rules) and `git status --short`.
2. Discover the nearest existing analogue to the requested behavior; inspect its callers, tests and contracts.
3. Declare an **allowlist of paths and behaviors**. Treat everything outside it as out of scope.
4. Identify protected boundaries: core, framework, architecture, public APIs, DB, auth, CI, dependencies, shared config, and moves/renames.
5. If a protected surface is unavoidable, **STOP WITHOUT EDITING THAT SURFACE** and propose safer alternatives. A user task request is not automatically approval to change core.

## Change rules

- Prefer additive, feature-local implementation and dependency injection or adapters **only if already supported by the project**.
- No sweeping cleanup, whole-file formatting, restructuring, filename moves, schema changes or package upgrades as incidental work.
- Never overwrite an existing uncommitted change. If a target is already modified, isolate and preserve it or report the collision.
- Validate relevant tests and report commands, outcomes and limitations. Never modify the test expectations to conceal a regression.

## Required final report

- Observed architecture and affected dependencies (with file references).
- Paths changed and explicit reason for each.
- Contracts preserved, tests run/results, tests not run.
- Protected changes **not performed** and recommended alternatives, if any.

## Technical gate

Use `scripts/change_guard.py` from the plugin distribution for snapshot/verify when available. Ask the project owner to control the approval file and baseline outside the agent's write access; a self-administered check is only advisory.
