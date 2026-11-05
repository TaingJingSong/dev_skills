---
name: fastapi-generate-core-structure
description: Extend FastAPI backends using existing project route, ORM, schema and service patterns. Use for Python/FastAPI feature scaffolding; preserve the current structure.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# FastAPI Generate Core Structure

Generate the smallest safe structure required by the request. Preserve the repository's architecture. Leave unknown business behavior as explicit TODOs.

## Procedure

### 1. Inspect

Read the repository and inspect the target area plus one or two maintained analogous features. Determine:

- Module and file organization.
- Router and registration style.
- Pydantic, SQLAlchemy, and sync/async conventions.
- Logic boundaries — logic always stays in `views.py`; no service or repository layer.
- Database session ownership — always `from core.db_session import get_db`.
- Authentication, permission, and data-scope dependencies.
- Response envelopes and exception handling.

If the repository cannot be inspected, use the baseline in `references/baseline.md`.

### 2. Plan

Classify as one of: New Feature, Existing Feature Update, Bug Fix Structure, Refactor Structure, API Structure, Database Model Structure, Integration Structure, Background Job Structure, Report or Export Structure.

Choose one strategy:
1. Extend the existing target module.
2. Follow the closest maintained feature.
3. Create a minimal module using the dominant repository pattern.
4. Use `references/baseline.md` when no repository evidence is available.

List required files and unresolved assumptions before generating code. Do not create optional layers "just in case."

### 3. Generate

Create or modify only the files required by the plan.

- Follow existing imports, naming, dependency injection, routing, response, error, auth, and test patterns.
- Logic always in `views.py` — do not create `service.py` or `repository.py`.
- DB session: always `from core.db_session import get_db` — never redefine it.
- Router registration: append `from .<module>.views import *` to `api/app/register.py` or `api/mobile/register.py`.
- Add models and schemas only from confirmed fields.
- Reuse existing auth and permission dependencies; otherwise add a visible TODO.
- Add `utils.py` only when reusable logic appears across multiple endpoints within the module.
- Add a migration reminder when schema changes are required.
- Use concise TODOs that name the missing requirement.

When the user asks to create, add, implement, scaffold, or update workspace code, edit the files directly. When the user requests only an example, proposal, or explanation, return code blocks without editing.

### 4. Validate

Run the narrowest repository-supported checks. Fix failures caused by the change and rerun.

Verify before finishing:
- File set matches the plan.
- Imports and router registration are complete.
- No business rules, fields, permissions, or migration behavior were invented.
- No unrelated files changed.
- TODOs clearly identify unresolved requirements.

## Custom Endpoint Response Pattern

Every custom endpoint (one that does not use the standard CRUD API) **must** use one of three response functions. Choosing the wrong one is a violation.

### Core files to inspect before generating any module

| File | What to read for |
|------|-----------------|
| `core/crud_api.py` | CRUDAPI constructor signature, `init_route()` routes, `disable_route` options |
| `core/crud_post.py` | `before_save()` hook signature and return contract |
| `core/crud_put.py` | `before_update()` hook signature |
| `core/crud_list.py` | `get_header()` format, `list_all`, `get_list_query()` |
| `core/crud_view.py` | `get_view_query()` override pattern |
| `core/crud_helper.py` | Shared utilities available to all subclasses |
| `core/constants.py` | `RecordType`, `RecordEditType`, `ExportType`, `ApproveSchema`, `RevertSchema` |
| `core/security.py` | `User`, `get_current_active_user`, `Annotated` |
| `core/db_session.py` | `get_db()` — always import from here, never redefine |
| `core/lib.py` | `check_role_permission()`, `set_user_activity_log()`, `getLang()` |
| `core/model.py` | Base model class — check before defining any new SQLAlchemy model |

## CRUDAPI Class-Based Pattern (Primary)

Use for all standard CRUD modules. Manual routers are only for custom
reports, background jobs, or non-standard integrations that cannot fit
the standard list/view/create/update/delete/approve flow.

### Minimal subclass

```python
from main import app
from core.crud_api import *
from .models import *
from .schemas import *

class FEATURE_CRUDAPI(CRUDAPI):
    query_fields = ['name']  # fields searched by /query endpoint
    list_all = True          # omit or False to scope by company

    def get_header(self):
        return [
            {"field": "id",   "text": "ID",   "width": "20%", "align": "center", "sortable": True,  "searchable": True},
            {"field": "name", "text": "Name", "width": "80%", "align": "left",   "sortable": False, "searchable": True},
        ]

    def before_save(self):
        # self.item = payload dict, self.db, self.current_user available
        error_list = {}
        exists = self.db.query(TBL_MODEL).filter(
            TBL_MODEL.name == self.item.get('name'),
            TBL_MODEL.id   != self.item.get('id'),
            TBL_MODEL.company_id == self.current_user.token_working_company_id
        ).first()
        if exists:
            error_list['name'] = 'Name already exists'
        if error_list:
            raise ValueError(error_list)
        return True, ''

    def before_update(self):
        return self.before_save()

crud = FEATURE_CRUDAPI('ModuleName', 'url-slug', TBL_MODEL, {}, schema=FeatureSchema)
crud.init_route()
app.include_router(crud.router, prefix="/api/v1", tags=['Feature'])
```

### Disabling routes

```python
crud.init_route(disable_route=['approve', 'reject', 'revert', 'export', 'import', 'template'])
```

### Decision rule

```
Is the result a paginated list of rows?
├── YES → Does it need computed SQL expressions (subqueries, aggregates, JSON) as columns?
│         ├── YES → customFilterWithCustomFields(obj, headers, model, field_summary, ...)
│         └── NO  → customFilter(obj, headers, model, {}, module_name, ...)
└── NO  → response_msg(...)
```

When in doubt: if the endpoint returns a single object, a computed scalar, or a non-paginated result → `response_msg`. If it returns plain model field rows → `customFilter`. If it returns rows with extra computed columns → `customFilterWithCustomFields`.

### `customFilterWithCustomFields` — paginated list with computed columns

Use when the query selects from a base model but needs extra columns built from SQL expressions (subqueries, aggregates, `case`, `func.*`, JSON aggregations).

```python
from lib.utils import customFilterWithCustomFields

headers = [
    # Plain model field
    {'field': 'id', 'label': 'leave_type_id', 'text': 'Leave Type ID'},
    # Field from a joined model
    {'field': 'id', 'model': TBL_USER, 'label': 'user_id', 'text': 'User ID'},
    # Concatenated fields
    {
        'field': '',
        'concat': [{'field': 'first_name'}, {'field': 'last_name'}],
        'label': 'employee_name',
        'text': 'Employee Name',
    },
    # Concatenated with a URL prefix separator
    {
        'field': '',
        'concat': [{'field': 'profile_picture', 'separator': f"{os.getenv('APP_URL', '')}/static/images/User/"}],
        'label': 'profile_picture',
        'text': 'Profile Picture',
    },
    # SQL expression column
    {'func': used_amount_expr, 'label': 'used_amount', 'text': 'Used Amount'},
]

return customFilterWithCustomFields(
    obj=base_query,           # db.query(TBL_SOME_MODEL).filter(...)
    header=headers,
    model=TBL_SOME_MODEL,     # the primary model the query is built from
    field_summary=None,
    module_name="Human Readable Module Name",
    filter=filter,
    sort=sort,
    search=search,
    page=page,
    size=size,
    full_summary=False,
    custom_summary={          # optional — flat dict of extra top-level response fields
        "month": selected_month.strftime("%Y-%m"),
    },
)
```


### `customFilter` — paginated list, plain model fields only

Use when the query returns rows with no computed SQL columns — plain fields, joined model fields, or concatenations only.

```python
from lib.utils import customFilter

headers = [
    {"field": "id",   "label": "record_id", "text": "Record ID"},
    {"field": "name", "text": "Name"},
    # joined model field
    {"field": "id", "model": TBL_OTHER, "label": "other_id", "text": "Other ID"},
    # concatenation
    {
        "field": "",
        "concat": [{"field": "first_name"}, {"field": "last_name"}],
        "label": "full_name",
        "text": "Full Name",
    },
]

return customFilter(
    obj,          # db.query(TBL_MODEL).filter(...)
    headers,
    model,        # TBL_MODEL
    {},           # always empty dict
    module_name,  # "Human Readable Module Name"
    filter,
    sort,
    search,
    page,
    size,
)
```

### `response_msg` — single result or non-paginated data

Use when the endpoint returns one computed result, a single object, or a flat data dict — not a paged list.

```python
from lib.render_api import response_msg

return response_msg(
    status=True,
    code=200,
    title="Human Readable Title",
    msg="You have successfully retrieved <resource>",
    error=None,
    data={
        # TODO: confirm fields from business requirements
    },
)
```

### Rules

- Always inspect `core/crud_api.py` before scaffolding any module to confirm the current constructor signature.
- Only read mixin files (`crud_post.py`, `crud_put.py`, etc.) for the specific hook being overridden — not all upfront.
- Never reimplement routes that `init_route()` already provides.
- Never add a manual router for a module that fits the standard CRUDAPI flow.

## Gotchas

- **Wrong base class:** Do not scaffold a manual router for a module that fits CRUDAPI — use the subclass pattern and `init_route()`.
- **Logic in views.py only:** Do not create `service.py` or `repository.py` — this project keeps all logic in `views.py`.
- **DB session:** Never redefine `get_db`. Always import from `core.db_session`.
- **Unknown fields:** Omit concrete fields and leave a TODO. Never guess columns, relationships, constraints, or response shapes.
- **Existing feature update:** Extend the current module — do not create a parallel module.
- **Migration:** Add only a reminder unless the exact schema change is confirmed.
- **`utils.py`:** Only create when logic genuinely repeats across multiple endpoints. Do not pre-emptively scaffold it.
- **Raw response:** Never return a plain dict or Pydantic model directly — always use `response_msg`, `customFilter`, or `customFilterWithCustomFields`.
- **Wrong response function:** Returning a paged list via `response_msg` or a single result via a filter function is a violation — follow the decision rule in the Custom Endpoint Response Pattern section.
- **Invented `custom_summary` fields:** Only include fields explicitly confirmed by requirements — never guess extra summary keys.
- **Python value as `func` header:** SQL expression columns must be `.scalar_subquery()` — never pass a computed Python value.

## Boundaries

- Do not invent business logic, validation rules, API fields, database fields, permissions, or integration behavior.
- Do not force full CRUD, a service layer, repository pattern, or new architecture.
- Do not expose or hardcode credentials, tokens, secrets, or identifiers.
- Do not change authentication, authorization, session, or transaction behavior without clear instruction.
- Do not add dependencies unless explicitly required.
- Do not claim TODO-based scaffolding is a complete implementation.

## Response Template

```
## Project Pattern Observed
- Architecture:
- Similar feature:
- Relevant conventions:

## Task Classification
- Type:
- Strategy:
- Affected areas:
- Required files:

## Assumptions
- Confirmed:
- Unresolved:

## Proposed File Structure
<new and modified files only>

## Generated Core Structure
<summary of direct edits, or labeled code blocks when files were not edited>

## TODOs
- <remaining business, contract, permission, migration, or test work>

## Validation
- <checks run and results>

## Safety Check
- <confirm no invented requirements, unsafe migrations, dependencies, or unrelated changes>
```