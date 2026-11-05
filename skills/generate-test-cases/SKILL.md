---
name: generate-test-cases
description: Create systematic manual QA test plans for code, APIs, screens and workflows. Use for scenario tables and coverage matrices, not executable tests or defect audits.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# Generate Test Cases

Produce a structured, **exhaustive** list of test cases for given code or a feature/flow, in the QA test-plan table format below. The output is a checklist of scenarios (what to test and why), not test code. This is useful as a planning step before writing actual tests, as a code review artifact, or as a QA handoff document that can be pasted directly into a test-case spreadsheet.

## Exhaustiveness is the point

The single biggest failure mode for this skill is stopping early with a "reasonable-looking" list that actually only covers the obvious cases. Treat every test case list as incomplete until proven otherwise:

- Do not stop at one happy-path case and one error case per feature/function. Real coverage usually needs 5-15+ cases per non-trivial screen, endpoint, or function.
- Systematically walk every field, button, validation rule, branch, and state transition and ask "what test case does this line/element require?" before moving on.
- For every rule involving a number or threshold (age limits, leave-day thresholds, timeouts, retry counts), generate boundary cases at, just below, and just above the threshold — don't just pick one round-number example.
- For every yes/no business rule (allowed/blocked, approved/rejected, visible/hidden), generate both the case where it holds and the case where it doesn't.
- Before finalizing, do a second pass: list every distinct condition, field, and action you found during analysis in one column and check off which test case(s) cover it. Anything unchecked needs a new row, not a shrug.
- When in doubt about whether a scenario is "worth" including, include it — a QA reader can deprioritize a row, but can't test a row that was never written.

## Process

### 0. Identify the input type

- **Code** (a function, endpoint, widget, class) → do the structural code analysis in step 1.
- **Feature / screen / user flow** (a product feature, app screen, user journey, spec, or BRD/FRD excerpt) → do the flow analysis instead: walk every screen state, field, button, validation rule, permission/role variant, and business rule threshold mentioned or implied. Treat each distinct user-facing action and each distinct system rule as its own branch to cover, the same way a conditional is a branch in code.

Either way, the goal is the same: a full inventory of decision points, then a test case for every meaningfully distinct outcome at each one.

### 1. Read the code structurally

Don't just skim for intent — trace the control flow. For each function, method, endpoint, or component in scope, identify:

- **Signature**: parameters, types, optional/nullable fields, default values, return type(s)
- **Branches**: every `if`/`else`/`switch`/`case`/ternary — each branch is at least one test case, and each condition needs both a true and a false case
- **Loops**: zero iterations, one iteration, many iterations, and (if bounded) the boundary count
- **Exception handling**: every `try`/`catch`/`throw`/`raise`/`.catch()` — what triggers it, and whether it's re-thrown, swallowed, or transformed
- **External dependencies**: API calls, DB queries, file I/O, network requests — what happens on success, timeout, error response, empty response
- **State mutations**: anything read/written to a shared variable, cache, database, or global/singleton — order-dependence and idempotency matter here
- **Concurrency**: anything async, threaded, or with race-condition potential (shared mutable state accessed from multiple call sites)
- **Security-sensitive spots**: auth checks, permission checks, input sanitization, injection surfaces (SQL, shell, path traversal), rate limiting

If the code spans multiple functions/files, group the output by function/endpoint/component rather than producing one flat list.

### 2. Enumerate across these categories

For each unit identified in step 1, generate candidates in each relevant category. Skip categories that plainly don't apply (e.g., no concurrency category for a pure synchronous string-formatting function) rather than padding the list.

| Category | What to look for |
|---|---|
| Happy path | Typical valid input producing the expected, unremarkable result |
| Boundary / edge values | Empty string/list/object, zero, negative numbers, min/max limits, single-element collections, exact threshold values, off-by-one around any comparison (`<` vs `<=`) |
| Invalid / malformed input | Wrong type, out-of-range values, malformed strings (bad email/date/format), unexpected extra fields |
| Null / missing data | Null/None/undefined parameters, missing optional fields, missing required fields |
| Error / exception paths | Every catch/throw path — both the trigger condition and the resulting behavior (error message, status code, rollback) |
| State-dependent behavior | Behavior that differs based on prior calls, ordering, or cached/stale state; idempotency (calling twice = calling once?) |
| Concurrency | Simultaneous calls racing on shared state, double-submit, partial writes |
| Integration / external failure | Downstream timeout, 4xx/5xx response, empty/malformed response, retries |
| Security | Unauthorized/unauthenticated access attempts, permission-boundary crossing, injection payloads, oversized payloads |
| Performance (only if relevant) | Very large input size, pagination limits, N+1-triggering data shapes |

### 3. Trace coverage explicitly before finalizing

Go back through every conditional (for code) or every rule/field/button (for a feature) and confirm each one has a test case exercising every meaningfully distinct outcome. This catches the common gap where the happy path and one error case are covered but a middle branch, a secondary field, or a "what if the user does X instead" path is missed. This is the step that turns a plausible-looking list into an exhaustive one — do not skip it.

## Output format

Match this exact table structure — it mirrors a standard QA test-plan spreadsheet and can be pasted directly into one. Group rows by **Feature** (a screen, module, or logical area). Within each feature, assign a short uppercase prefix derived from the feature name (e.g., "Login/Authentication" → `UA`, "Attendance" → `ATT`, "Leave" → `LE`, "Home Screen" → `HS`) and number sequentially: `PREFIX-001`, `PREFIX-002`, ... If the user has existing IDs/prefixes already in use (e.g., they paste an existing sheet or mention conventions), reuse those instead of inventing new ones.

```markdown
| Test ID | Feature | Scenario ID | Scenario Title | Scenario Status | Precondition | Test Step | Test Data | Expected Result |
|---|---|---|---|---|---|---|---|---|
| 1 | Login | UA-001 | Login with valid credentials | Positive | User is on the login screen | Enter valid username and password, tap Login | Username: jing / Password: valid | User is logged in and redirected to Home |
| | Login | UA-002 | Login with incorrect password | Negative | User is on the login screen | Enter valid username, wrong password, tap Login | Username: jing / Password: wrong | Error message "Invalid credentials" shown, login blocked |
| | Login | UA-003 | Login with empty username | Negative | User is on the login screen | Leave username blank, enter password, tap Login | Username: (empty) | Validation error "Username required", login blocked |
| | Login | UA-004 | Account locked after repeated failures | Negative | User has failed login 2 prior times | Enter wrong password a 3rd time | Failed attempts: 3 | Account locked, message "Account locked" shown |
```

Column meanings:
- **Test ID**: sequential number for the feature *group* — only filled on the group's first row (matches the reference template, where it reads as a group header down the left column)
- **Feature**: the screen/module/component name
- **Scenario ID**: `PREFIX-###`, unique and sequential per feature
- **Scenario Title**: short human-readable name for the scenario
- **Scenario Status**: `Positive`, `Negative`, or `Positive & Negative` (use the latter only when a single scenario genuinely has to validate both an accepted and a rejected path together, e.g., a boundary that splits behavior)
- **Precondition**: state the system/user must already be in before the test step
- **Test Step**: numbered actions the tester performs
- **Test Data**: concrete example values — never leave this vague when the scenario depends on specific numbers/thresholds
- **Expected Result**: the observable outcome, specific enough that "pass" vs "fail" isn't ambiguous

Leave out QA-tracking columns (Actual Result, Bugs Report, Test By, Status, Assigned Developer, Fix Status) unless the user asks for them — those get filled in during actual test execution, not during generation.

After the table(s), add a short **Coverage notes** section (2–5 bullets) calling out:
- Any branch/rule you couldn't find a clean test case for and why
- Any assumption made about ambiguous behavior (e.g., "assumed negative age should be rejected — confirm business rule")
- Any category or feature area intentionally skipped and why

## Delivering as a file

If the user wants a downloadable spreadsheet (not just an inline table) — e.g. "give me a file," "make it a sheet I can import," or the test plan is large — use the `xlsx` skill to build an actual `.xlsx` with the same columns as headers, one feature group per visual block (blank Test ID cells after the first row of each group, exactly as in the table above), and reasonable column widths/wrapping so Test Step and Expected Result are readable. Don't build a custom exporter — the xlsx skill already covers formatting, headers, and column widths correctly.

## Before you present the result: definition of done

Check every item before finalizing, and fix anything unchecked rather than shipping a partial list:

- [ ] Every field/parameter mentioned in the code or spec has at least one test case exercising an invalid/missing value for it
- [ ] Every conditional/business rule has a test case for each outcome it can produce, not just the two most obvious ones
- [ ] Every numeric threshold has a case at the boundary, one step below, and one step above
- [ ] Every user-facing error message or validation state referenced in the code/spec appears as an Expected Result somewhere
- [ ] No two rows are testing the exact same underlying condition through different wording
- [ ] Scenario IDs are sequential and consistently prefixed within each feature group
- [ ] The Coverage notes section flags every assumption or gap you weren't able to resolve from the given code/spec alone

## Guardrails

- Don't invent business rules the code/spec doesn't imply — if behavior is ambiguous, write the test case with the ambiguity flagged in Coverage notes rather than silently guessing.
- Don't generate near-duplicate rows (two cases that would pass/fail together for the same underlying reason) — each row should catch a distinct bug class or cover a distinct rule.
- Favor more rows over fewer when genuinely distinct conditions exist — see "Exhaustiveness is the point" above. A shorter list is only better if every row that was cut was truly redundant, not just less interesting.
- If the user pastes a very large file/module or an entire multi-screen app, ask which function(s)/screen(s) they want covered before enumerating everything, unless they've already said "all of it."