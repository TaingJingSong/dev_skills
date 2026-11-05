---
name: minimal-change-enforcer
description: Implement the smallest approved code diff using established repository patterns. Use for scoped feature work and bug fixes while protecting core and unrelated files.
---

# Minimal Change Enforcer

## Before editing

- Confirm user outcome and acceptance criteria; inspect current Git status and similar implementations.
- Define exact target paths, permitted changes and tests. If approval is ambiguous, choose the smaller non-destructive scope.
- Run project-context and impact checks mentally or by invoking relevant skills when the agent supports them.
- Stop and report if core, architecture, contracts, DB schema, dependencies or protected paths must change.

## During editing

- Modify the smallest number of in-scope lines/files. Prefer local adapters and extension points the repo already uses.
- Match formatting/style already present. Preserve public behavior for unaffected callers.
- No rename, move, whole-file formatting, unrelated refactor, dependency churn, CI/config edits or migration unless explicitly approved and within policy.
- Do not touch unrelated dirty working-tree paths; avoid blanket commands that rewrite unrelated files.

## After editing

- Inspect precise `git diff`, files added/deleted and Git status. No unexpected paths should remain.
- Execute targeted tests, relevant regression checks and linters where feasible; do not weaken existing tests.
- If checks fail, report accurately; do not claim complete verification.
- Return changed-file inventory, rationale, compatibility notes and tests. Report deferred protected changes as suggestions, not modifications.
