---
name: change-impact-analyzer
description: Trace the blast radius of a proposed code change across APIs, data, clients, security, jobs and tests. Use before risky edits; return a read-only impact report.
---

# Change Impact Analyzer

## Read-only procedure

1. Define requested behavior and enumerate candidate in-scope paths.
2. Trace direct callers, importers, handlers, consumers and persistent data flows; search for parallel routes and mobile/web clients.
3. Check contract changes: request/response, events, schema/migrations, validation, auth/permissions, concurrency/idempotency and backwards compatibility.
4. Check test surfaces, release/deploy implications and failure/rollback scenarios, distinguishing supported facts from hypotheses.
5. Separate additive low-risk changes from protected high-risk changes; identify feasible alternatives that preserve the current architecture.

## Output

| Surface | Current behavior / evidence | Proposed effect | Severity | Required tests | Approval |
|---|---|---|---|---|---|

Summarize a safe implementation boundary and a **BLOCKED — APPROVAL REQUIRED** section for any protected changes. Never write or stage changes during impact analysis.
