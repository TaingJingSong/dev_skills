# FastAPI Framework Baseline

Use only when repository inspection yields no evidence (blank workspace or new project).
When an existing repo is present, always prefer what inspection reveals.

## Project-level layout

<project_name>/
├── main.py               # App factory — mounts FastAPI instances, registers middleware
├── config.py             # Settings / env loading (Pydantic BaseSettings)
├── celeryconfig.py       # Celery broker and backend config
├── tasks.py              # Root-level Celery task definitions
├── core/
│   └── db_session.py     # get_db() dependency — always import from here, never redefine
├── api/
│   ├── app/
│   │   ├── register.py   # Wildcard-imports every module's views.py
│   │   └── <module>/
│   │       ├── models.py
│   │       ├── schemas.py
│   │       └── views.py
│   └── mobile/           # Add only when a separate mobile FastAPI instance is needed
│       ├── register.py
│       └── <module>/
│           ├── models.py
│           ├── schemas.py
│           └── views.py
└── requirements.txt
```

## Module layout (one feature)

```
api/app/<module>/
├── models.py     # SQLAlchemy ORM models
├── schemas.py    # Pydantic request / response shapes
├── views.py      # Route handlers + all business logic
└── utils.py      # Optional — reusable helpers (only when genuinely reused across endpoints)
```

## Registration pattern

```python
# api/app/register.py
from .login.views import *
from .faq.views import *
# from .<new_module>.views import *  ← append here when adding a module
```

## DB session usage

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from core.db_session import get_db

@router.get("/example")
def example(db: Session = Depends(get_db)):
    ...
```

## Auth / permission placeholder

```python
# TODO: replace with the correct auth dependency once confirmed
current_user = Depends(...)
```

## Custom Endpoint Response Functions

### Decision tree

```
Paginated list of rows?
├── YES + computed SQL columns (subqueries, aggregates, JSON) → customFilterWithCustomFields(obj, headers, model, field_summary, ...)
├── YES + plain model fields only                             → customFilter(obj, headers, model, {}, module_name, ...)
└── NO (single object, scalar, flat dict)                    → response_msg(...)
```

### `customFilter` skeleton

```python
from lib.utils import customFilter

return customFilter(
    obj,          # db.query(TBL_MODEL).filter(...)
    headers,      # list of plain field / concat header dicts
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

### `customFilterWithCustomFields` skeleton

```python
from lib.utils import customFilterWithCustomFields

headers = [
    {'field': 'id',   'label': 'record_id',   'text': 'Record ID'},           # plain field
    {'field': 'id',   'model': TBL_OTHER,  'label': 'other_id', 'text': ''},  # field from joined model
    {'field': '', 'concat': [{'field': 'first_name'}, {'field': 'last_name'}],
     'label': 'full_name', 'text': 'Full Name'},                               # concatenated fields
    {'field': '', 'concat': [{'field': 'picture', 'separator': f"{os.getenv('APP_URL','')}/static/images/User/"}],
     'label': 'profile_picture', 'text': 'Profile Picture'},                   # field with URL prefix
    {'func': some_scalar_subquery, 'label': 'computed_col', 'text': 'Label'},  # SQL expression
]

return customFilterWithCustomFields(
    obj=db.query(TBL_MODEL).filter(...),
    header=headers,
    model=TBL_MODEL,
    field_summary=None,
    module_name="Module Name",
    filter=filter, sort=sort, search=search, page=page, size=size,
    full_summary=False,
    custom_summary={"key": value},  # only confirmed fields
)
```

### `response_msg` skeleton

```python
from lib.render_api import response_msg

return response_msg(
    status=True,
    code=200,
    title="Title",
    msg="You have successfully retrieved <resource>",
    error=None,
    data={
        # TODO: confirm fields
    },
)
```