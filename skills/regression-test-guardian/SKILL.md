---
name: regression-test-guardian
description: Plan and run relevant tests for approved changes. Use after implementation or during review to verify regressions, preserve existing tests and report actual outcomes.
---

# Regression Test Guardian

## Workflow

1. Inspect changed paths, control/data flow, callers, contracts and historical tests.
2. Map success paths, error paths, edge boundaries, permissions, concurrency/idempotency, migration compatibility and downstream consumers to existing tests.
3. Run the smallest relevant suite first; broaden to neighboring integration/regression suites when available.
4. Add tests only when in scope; keep production tests intact. Never edit an existing test merely to make a new implementation pass without explaining the changed expected behavior and obtaining approval.
5. Record exact commands, exit status, evidence and skipped checks. Distinguish a missing test from a passing test.

## Report

| Scope | Check/command | Outcome | Evidence/notes |
|---|---|---|---|

Finish with **Verified**, **Unverified**, **Known failures** and **Protected changes required**. If no runtime or dependencies are available, provide reproducible commands without claiming they ran.
