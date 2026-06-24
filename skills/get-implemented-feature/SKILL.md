---
name: get-implemented-feature
description: Quickly capture the actual backend contract from implemented code for frontend/mobile consumption. Use after backend implementation is complete when a lightweight snapshot is enough. Produces a concise note focused on API contract, validation, list behavior, and notable frontend/mobile concerns.
---

# Get Implemented Feature

Generate a compact contract snapshot from the implemented backend code.

The goal is to document what was actually built, not what was originally planned.

## When To Use

Use after backend implementation is complete and frontend/mobile work needs to consume the feature.

Do not use for planning.

If implementation does not yet exist, use generate-implementation-prompt instead.

---

## Read

Locate and inspect the implementation files.

Prioritize:

- models.py
- schemas.py
- views.py / routes.py
- validation logic

Read tests only if validation behavior is unclear.

---

## Extract

Capture only information that affects API consumers.

### Endpoints

For each endpoint include:

- Method
- Path
- Purpose
- Auth requirement (if obvious)

### Request Shape

For each field include:

- Name
- Type
- Required/Optional
- Constraints (max length, enum, format)

### Response Shape

Only document fields returned to clients.

### Validation

Capture actual validation rules:

- Uniqueness checks
- Required conditions
- Business rules
- Scope rules (company/user scoped)

### List Behavior

Only if applicable:

- Pagination params
- Filtering params
- Sorting params

---

## Frontend Notes

Only include non-obvious behavior such as:

- Duplicate checks are company-scoped
- Soft delete exists
- Empty state expected
- Feature partially implemented

Maximum 5 bullets.

---

## Ignore

Do not include:

- Internal helper functions
- ORM details
- Database indexes
- Implementation reasoning
- Speculation
- Long explanations
- Full plan diffs

---

## Output

Save to:

docs/contracts/<feature-name>.md

Use this format:

```text
# Contract Snapshot: <Feature Name>

Source:
- <files read>

## Endpoints
- GET /path
- POST /path

## Request
- field: type, required, constraints

## Response
- field: type

## Validation
- validation rule

## List Behavior
- pagination/filtering/sorting

## Frontend Notes
- important behavior
```

Keep output under 300 words whenever possible.

---

## Example

```text
# Contract Snapshot: ReasonType

Source:
- api/reason_type/models.py
- api/reason_type/views.py

## Endpoints
- GET /api/v1/wb/reason-type
- POST /api/v1/wb/reason-type
- PUT /api/v1/wb/reason-type/{id}

## Request
- name: string, required, max 100

## Response
- id: string
- name: string

## Validation
- name must be unique within company

## Frontend Notes
- company scoped
- no seed data exists
```
