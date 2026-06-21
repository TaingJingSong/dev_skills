---
name: generate-contract-snapshot
description: Capture what a backend feature actually shipped — not what was planned — as a single grounded handoff file for frontend/mobile implementation. Use after a backend task is implemented (not before), when frontend or mobile work needs to consume the result. Reads the real implemented code (models, schemas, routes, validation) rather than the original implementation prompt, since plans drift during implementation. Output feeds directly into generate-implementation-prompt's Source References for the next platform.
---

# Generate Contract Snapshot

Produce one grounded handoff file documenting what a backend feature actually built, so a frontend or mobile implementation prompt can be generated against reality instead of a stale plan or guesswork.

This skill runs *after* backend implementation is done, never before. If the backend isn't implemented yet, there's nothing to snapshot — point the requester at `generate-implementation-prompt` for the backend task instead.

## Why this exists

An implementation prompt describes intent. Implementation can legitimately diverge from intent — a field gets renamed during review, a validation edge case gets added, an endpoint path changes to match an existing convention. If frontend/mobile work is grounded in the *original prompt*, it inherits any drift as if it were still true. This skill re-derives the contract from the actual shipped code, so the next platform starts from what's real.

## Procedure

### 1. Locate the Implemented Feature

Identify the actual files that implement the feature in question — not the implementation prompt that requested it. If a `map-platform-structure`-style backend cache exists, use it to find the right module fast; otherwise locate via the obvious naming match (e.g. a feature called "ReasonType" → `api/reason_type/`).

Read, at minimum:

- The model/schema definition (exact field names, types, lengths, nullability, defaults).
- The route/view layer (exact endpoint paths, HTTP methods, request/response shape).
- Validation logic (what's actually enforced — not what the prompt asked for, what the code does).
- Any serializer/response-mapping layer if requests and responses aren't the same shape as the model.

If tests exist for this feature, read them too — they often reveal real edge-case behavior (what happens on duplicate, on missing field, on permission failure) faster and more reliably than reading application code alone.

### 2. Diff Against the Original Plan (if available)

If the original implementation prompt for this feature is available (e.g. from `generate-implementation-prompt`'s prior output), compare it against what was actually built. Capture only real differences:

- Fields that were renamed, added, dropped, or retyped from the plan.
- Validation rules that were tightened, loosened, or scoped differently than planned.
- Endpoint paths, methods, or response envelopes that differ from what was specified.

If no original prompt is available, skip this — do not reconstruct a fictional plan to diff against. State plainly that no prior plan was available for comparison.

Never present an assumption about *why* something changed (e.g. "probably for security") — state only the observed difference. Motive is not observable from code.

### 3. Extract the Contract

Capture only what is directly observable in code:

- **Endpoints**: exact path, method, auth/permission requirement if visible in route decorators/dependencies.
- **Request shape**: exact field names, types, required vs. optional, defaults, constraints (max length, format).
- **Response shape**: exact field names and types returned — note if this differs from the request shape (e.g. server-generated fields like `id`, `created_at`).
- **Validation behavior actually enforced**: what triggers a 400/422, what the error shape looks like (field-level vs. general message), what's scoped by company/tenant/user vs. global.
- **Enum or fixed-value fields**: the actual allowed values, if defined in code (not guessed).
- **Pagination/filtering/sorting behavior**, if the endpoint is a list endpoint: exact query params accepted and their defaults.
- **Side effects**: anything beyond the direct CRUD operation that frontend/mobile should know about (e.g. a webhook fires, a related record updates, a cache invalidates) — only if visible in the code, not inferred.

Do not include implementation details that don't affect a frontend/mobile consumer (internal helper function names, ORM-specific mechanics, unrelated database indices).

### 4. Note What Frontend/Mobile Cannot Infer From the Schema Alone

This is the section that most distinguishes this skill from "just read the API contract." Capture anything a consumer would otherwise have to guess or discover the hard way:

- Default sort order on list endpoints, if not obvious from params.
- Whether duplicate/conflict checks are case-sensitive, trimmed, or scoped in a non-obvious way.
- Whether soft-delete, history, or rejected-record variants exist and whether they're exposed via the same endpoint or a separate one.
- Any field that looks optional in the schema but is effectively required by business logic enforced elsewhere (e.g. defaulted server-side but expected to be set for the feature to behave correctly).
- Known gaps: anything the backend task explicitly deferred (e.g. "lookup-table integration not implemented yet, still using a free-text field") that frontend/mobile must not build against as if it exists.

If nothing nonobvious applies to a section, omit that section — do not pad with "Not applicable" lines; see the boundary on this below.

### 5. Write the Snapshot

Save to `docs/contracts/<feature-name>.md` (kebab-case feature name, matching the implementation prompt's task naming where possible, so the next platform's `generate-implementation-prompt` run can cite it by exact path).

Use the template below. Keep it dense — this is meant to be read once by a human and cited by path by another skill, not browsed casually.

### 6. Hand Off

State the file path plainly at the end of the response (e.g. "Contract snapshot written to `docs/contracts/reason-type.md`") so it can be passed directly into the next `generate-implementation-prompt` call as a Source Reference.

## Gotchas

- **Backend not actually finished**: If the code only partially implements the planned feature (e.g. create exists but update doesn't yet), document exactly what exists and flag the gap — don't snapshot the plan's intent for the missing parts.
- **Response shape differs from request shape**: Common with server-generated fields (`id`, timestamps, computed fields). Document both shapes explicitly rather than assuming symmetry.
- **Validation only enforced in one direction**: E.g. duplicate-name check exists on create but not update, or vice versa. State this precisely — it directly affects what frontend/mobile must handle.
- **Soft-launched or feature-flagged endpoints**: If the code shows a feature flag or conditional exposure, note it — frontend/mobile may need matching conditional logic.
- **No prior implementation prompt to diff against**: Common when the backend was implemented outside this skill set, or predates it. Proceed with extraction only (Step 3-4), skip Step 2 entirely, and say so.
- **Multiple consumers need different slices**: If frontend and mobile need different things from the same contract (e.g. mobile doesn't need an admin-only field), document the full contract once and let the consuming `generate-implementation-prompt` run select what's relevant — don't pre-filter the snapshot per platform.

## Boundaries

- Do not snapshot a feature that hasn't been implemented yet — that's planning, not capture, and belongs to `generate-implementation-prompt` instead.
- Do not infer or invent fields, validation, or behavior not directly observable in the code or its tests.
- Do not speculate about why an implementation differs from its plan — state the difference, not a motive.
- Do not suggest frontend/mobile UI treatment (e.g. "this should be a dropdown") — that's a frontend design decision belonging to the next platform's own implementation prompt, not a backend fact.
- Do not pad empty sections with "Not applicable" — omit sections with nothing to report so the snapshot stays dense and every line is signal.
- Do not treat the original implementation prompt as authoritative once code exists — code wins; the prompt is only used for diffing, never as a substitute for reading actual code.

## Output Template

```text
# Contract Snapshot: <Feature Name>

Source: <files actually read, e.g. api/reason_type/models.py, schemas.py, views.py>
Original plan available: <yes, diffed below / no, extraction only>

## Endpoints
- <METHOD> <path> — <one-line purpose>, auth: <requirement if visible>

## Request Shape
- <field>: <type>, <required/optional>, <constraints>

## Response Shape
- <field>: <type> (only if it differs from request shape — state the difference)

## Validation Behavior
- <rule actually enforced>: <trigger>, <error shape>

## Enum / Fixed Values
- <field>: <actual allowed values from code>

## List Behavior (if applicable)
- Pagination: <params and defaults>
- Default sort: <...>
- Filtering: <params>

## Side Effects
- <only if observed in code>

## What Changed From the Original Plan
(omit this whole section if no prior plan was available)
- <field/rule>: planned <X>, actually built <Y>

## What Frontend/Mobile Should Know
- <non-obvious behavior, gaps, deferred work — only items that apply>

## Not Yet Implemented
- <anything the original task scoped that the code doesn't yet cover, if applicable>
```

## Example

Input: backend feature "ReasonType" was implemented per a prior Full-tier implementation prompt; code now exists at `api/reason_type/`.

Output shape:

```text
# Contract Snapshot: ReasonType

Source: api/reason_type/models.py, schemas.py, views.py
Original plan available: yes, diffed below

## Endpoints
- GET /api/v1/wb/reason-type — list, auth: standard authenticated + company scope
- POST /api/v1/wb/reason-type — create, auth: standard authenticated + company scope
- PUT /api/v1/wb/reason-type/{id} — update, auth: standard authenticated + company scope

## Request Shape
- name: string, required, max 100
- name_lc: string, optional, max 100

## Response Shape
- id: string (server-generated, not in request)
- name, name_lc: as request
- plus standard CoreModel audit fields (created_at, updated_at, company_id)

## Validation Behavior
- Duplicate name check: company-scoped, enforced on both create and update (update excludes own id). Error returned as field-level: {'name': 'Reason Type <name> already exists'}.

## What Changed From the Original Plan
- id field: plan specified String(64); actual CoreModel uses String(42). Frontend/mobile should not assume a fixed id length beyond treating it as an opaque string.

## What Frontend/Mobile Should Know
- This is a standalone master-data module; it is not yet wired to the existing api/reason ReasonType enum. Do not build a feature that assumes these are the same data source.
- No seed data exists; list will be empty until records are created manually or via a future seed task.
```