---
name: analyze-edge-cases
description: Review code for real bugs, edge cases, security failures and robustness risks. Use for defect reviews and proposed fixes, not QA test case generation.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# Analyze Edge Cases & Propose Fixes

Given code, find every place it can fail, misbehave, or produce a wrong result — then propose a specific, minimal fix for each one. This is a defect-finding pass, not a test-planning pass: the deliverable is "here's what's wrong and here's the patch," not "here's what to test."

## Mindset

Read the code the way it will actually be exercised in production, not the way it was intended to be used. Most real bugs live in the gap between "what the author assumed the input/environment would look like" and "what it can actually look like." For every assumption the code makes — explicit or implicit — ask "what happens the moment this assumption is false?"

Don't just restate what the code does; simulate it. For each function/branch, mentally (or actually, via the bash tool if it's runnable) walk through the adversarial and degenerate inputs, not just the ones the author was clearly thinking about.

## Process

### 1. Understand the flow before hunting

Do not start looking for bugs until you can restate, in your own words, what this code is supposed to do and how data moves through it. Skipping this step is the main reason edge-case passes produce shallow or wrong findings — you can't tell what's broken if you don't know what "working" means here.

Build this understanding explicitly:
- **Purpose**: what is this function/endpoint/component for? Infer from naming, docstrings/comments, and — if visible — how callers use it and what the surrounding module does.
- **Control flow**: trace every path from entry to exit. For each branch point, note what condition sends execution which way, and what each exit point returns/does.
- **Data flow**: for each variable, trace where its value comes from (parameter, computed, fetched) and everywhere it's used or returned. Pay special attention to values that cross a boundary (function → caller, request → response, this service → another service/DB).
- **Implicit contract**: state, as if writing a spec, what this code promises given valid input (postconditions) and what it silently requires to be true beforehand (preconditions) — e.g. "promises `remaining` is never negative," "requires `available_days` to already be validated as non-negative by the caller." Write these down even though the code itself doesn't; they're what you'll check the implementation against in the next step.
- **Context, if available**: if related files, callers, or sibling functions are visible, skim them for how similar logic is handled elsewhere — this is often the fastest way to spot that *this* instance is missing a check that a sibling has.

Only once you can describe the intended behavior end-to-end should you move to hunting for where the actual implementation diverges from it.

### 2. Inventory every assumption

For each function, method, endpoint, or component in scope, list what it silently assumes about:
- **Input shape**: types, non-null, non-empty, in-range, correctly formatted, internally consistent (e.g. `end_date >= start_date`)
- **Call order / state**: that some other function already ran, that setup happened, that this isn't called twice, that it isn't called concurrently
- **Environment**: that a file/network/DB/service is reachable and fast, that a config value exists, that the clock/timezone is what's expected
- **Numeric behavior**: integer overflow/underflow, float precision/rounding, division by zero, sign handling
- **Resource limits**: unbounded loops/recursion, unbounded memory (loading a whole file/result set), unbounded string/array growth

### 3. Hunt in these categories

Work through each category against the actual code; skip categories that plainly don't apply rather than forcing a finding.

| Category | What to check |
|---|---|
| Boundary values | Off-by-one in comparisons (`<` vs `<=`), empty/zero/negative/max-value inputs, boundary of any threshold |
| Null / missing data | Every parameter and every field pulled from an object/response — what happens if it's null/undefined/missing |
| Type & format errors | Wrong type coerced silently, malformed strings (dates, emails, IDs) accepted or mishandled |
| Error handling gaps | Missing try/catch around I/O, catches that swallow errors silently, catches too broad (hiding real bugs), errors that leave state half-updated |
| Concurrency / races | Shared mutable state touched by more than one call path, check-then-act patterns without atomicity, double-submit |
| Resource & performance | Unbounded loops/recursion, N+1 queries, loading everything into memory, missing timeouts on external calls |
| Security | Unvalidated/unsanitized input reaching a query/shell/file path, missing auth/permission checks, secrets in logs, predictable IDs/tokens |
| Logic errors | Conditions that don't match the stated intent (inverted boolean, wrong operator, unreachable branch, dead code) — these are often the highest-value finds |
| Idempotency & retries | Would retrying this operation (network retry, duplicate webhook, page refresh) double-charge/double-create/corrupt state? |
| Internationalization / locale (if relevant) | Timezone assumptions, locale-dependent formatting/parsing, non-ASCII input |

### 4. Apply these additional techniques for deeper coverage

These catch classes of bugs the category sweep above tends to miss:

- **Contract violation check**: go back to the pre/postconditions you wrote in step 1 and check the implementation against them line by line — does every return path actually satisfy the postcondition you stated? (This is exactly how the negative-`remaining` bug in the example below was found: the stated postcondition "`remaining` is never negative" doesn't hold on the emergency-override return path.)
- **Mutation-thinking**: for each comparison operator, boundary constant, and boolean condition, ask "if this were subtly wrong (`<` instead of `<=`, `and` instead of `or`, off-by-one constant), would any existing test or code path catch it?" If no, that's both a latent-bug risk and a test-coverage gap worth naming.
- **Consistency / differential check**: if sibling functions, similar endpoints, or parallel platform implementations (e.g. the same validation rule implemented in FastAPI and in Flutter) are visible, compare their handling of the same rule. Divergent handling of the same business rule across places is a common real-world bug source.
- **Known-defect pattern matching**: check against recurring classes of real-world defects even if nothing above surfaced them — TOCTOU (time-of-check-to-time-of-use) gaps, resource/connection leaks (opened but not closed/released on error paths), unbounded cache growth, silent truncation on type conversion, timezone-naive datetime math.
- **Empirical verification**: when the code (or a minimal extraction of it) is actually runnable, use the bash tool to execute it against a handful of the suspected edge inputs rather than relying purely on reading. A confirmed trigger from actual execution is stronger evidence than reasoning alone, and takes the guesswork out of borderline cases.

### 5. For every finding, verify it's real before reporting it

Don't report a "bug" that's actually handled correctly elsewhere in the code (e.g., validated by a caller, or by a framework/decorator you can see in context). If you're not sure whether something is actually reachable, say so explicitly as a caveat rather than presenting speculation as a confirmed bug.

### 6. Propose a fix for each finding

For every real finding, propose the smallest correct fix — not a rewrite. Show it as a diff-style snippet (before/after) scoped to just the relevant lines, so it's easy to review and apply. If a proper fix requires a broader architectural change, say so explicitly and offer the minimal patch as a stopgap plus a one-line note on the larger fix.

## Output format

Start with a short **Understood flow** summary (3-6 sentences): what the code does, the key control/data flow paths, and the implicit contract you identified in step 1. This isn't filler — it's what lets the reader (including you, if you don't work in QA/testing day to day) judge whether a finding below is actually a real risk for how this code is used, or a misunderstanding on either side worth flagging back.

Then group findings by function/file, ordered by severity (Critical → High → Medium → Low) within each group.

```markdown
### `functionOrFileName`

#### 🔴 Critical — Negative remaining leave balance on emergency override
**Where:** the `is_emergency` branch when `requested_days > available_days`
**Problem:** approving an emergency request beyond the buffer check still returns `remaining = available_days - requested_days`, which can go negative — nothing downstream stops a negative balance from being persisted.
**Trigger:** `requested_days=7, available_days=5, is_emergency=True` → returns `remaining: -2`
**Fix:**
\`\`\`diff
- return {"approved": True, "reason": "emergency_override", "remaining": available_days - requested_days}
+ remaining = max(0, available_days - requested_days)
+ return {"approved": True, "reason": "emergency_override", "remaining": remaining, "deficit": max(0, requested_days - available_days)}
\`\`\`
**Why this fix:** clamps the reported balance at zero and surfaces the actual deficit separately, so callers can't accidentally persist a negative balance while still preserving the emergency-override information.

#### 🟡 Medium — ...
```

Severity guide:
- **Critical**: data loss/corruption, security exposure, crash affecting all users, financial/business-rule violation (e.g. the negative-balance example above)
- **High**: wrong result for a plausible, non-exotic input; unhandled exception that takes down a request
- **Medium**: wrong result only for rare/edge inputs; degraded UX; missing validation with a low-risk blast radius
- **Low**: style/robustness nits, defensive-programming suggestions, theoretical issues with no realistic trigger

After the findings, add a **Summary** with a one-line count per severity, and a short **Not flagged** note for anything you deliberately considered and ruled out (so the reader knows it was checked, not missed).

## Guardrails

- Every finding needs a concrete trigger (an actual input/sequence that causes it) — "this could theoretically be a problem" without a trigger belongs in Low/Not flagged, not Critical/High.
- Keep fixes minimal and in the same style/idioms as the surrounding code — don't introduce a new library, pattern, or restructure unrelated code as part of a bug fix.
- If two findings share one root cause, report the root cause once and list the multiple symptoms under it rather than duplicating the same fix.
- Don't flag something already correctly handled elsewhere in the visible code (validation decorators, framework-level guarantees, a caller that already checks). If unsure whether it's handled upstream, ask or state the assumption instead of asserting a false positive.
- If the file/module is large, ask which function(s) or which risk category (security vs. correctness vs. performance) to prioritize before analyzing everything, unless the user already said "all of it."