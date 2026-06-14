import json
from textwrap import dedent


SKILL_ROUTING = {
    "mobile": [
        "company-engineering-standard",
        "mobile-core-structure",
        "flutter-build-responsive-layout",
        "generate-implementation-prompt",
    ],
    "backend": [
        "company-engineering-standard",
        "fastapi-generate-core-structure",
        "generate-implementation-prompt",
    ],
    "frontend": [
        "company-engineering-standard",
        "frontend-core-structure",
        "generate-implementation-prompt",
    ],
    "fullstack": [
        "company-engineering-standard",
        "mobile-core-structure",
        "fastapi-generate-core-structure",
        "generate-implementation-prompt",
    ],
}


STACK_TARGETS = {
    "mobile": {
        "platform": "mobile",
        "framework": "flutter",
    },
    "backend": {
        "platform": "backend",
        "framework": "fastapi",
    },
    "frontend": {
        "platform": "web",
        "framework": "frontend",
    },
    "fullstack": {
        "platform": "fullstack",
        "framework": "mixed",
    },
}


def get_required_skills(
    target_stack: str,
    skill_names: list[str] | None = None,
) -> list[str]:
    if skill_names:
        return skill_names

    return SKILL_ROUTING.get(
        target_stack,
        [
            "company-engineering-standard",
            "generate-implementation-prompt",
        ],
    )


def get_stack_target(target_stack: str) -> dict:
    return STACK_TARGETS.get(
        target_stack,
        {
            "platform": target_stack,
            "framework": "unknown",
        },
    )


def get_rules_for_stack(target_stack: str) -> list[str]:
    base_rules = [
        "Inspect the current project before editing.",
        "Do not assume components, folders, routes, models, repositories, or services exist.",
        "Reuse existing project patterns where available.",
        "If a referenced skill is not available, continue by inspecting the project directly.",
        "If a reusable component does not exist, create a local screen-level widget/component first.",
        "Only promote to shared component if reused in multiple places.",
        "Add TODOs for missing API contracts or business rules instead of inventing behavior.",
    ]

    mobile_rules = [
        "For Flutter, verify whether CoreView<T>, CoreViewModel, GetIt, go_router, LangSingleton, ThemeViewModel, GlobalOverlay, and CustomSnackbarAlert exist before using them.",
        "Do not call Dio directly from UI.",
        "Use repository/view-model pattern if the project uses it.",
        "Do not hardcode user-facing labels if localization exists.",
    ]

    backend_rules = [
        "For FastAPI, inspect existing router, schema, service, model, CRUD, permission, and dependency patterns first.",
        "Do not invent request/response fields.",
        "Do not bypass existing authentication, authorization, or company-scope rules.",
        "Add TODOs for missing approval rules, permission rules, and data contracts.",
    ]

    frontend_rules = [
        "For frontend, inspect existing component structure, routing, state management, API client, theme, and localization patterns first.",
        "Reuse existing UI components if they exist.",
        "Do not invent API fields or hardcode labels if localization exists.",
    ]

    if target_stack == "mobile":
        return base_rules + mobile_rules

    if target_stack == "backend":
        return base_rules + backend_rules

    if target_stack == "frontend":
        return base_rules + frontend_rules

    if target_stack == "fullstack":
        return base_rules + mobile_rules + backend_rules + frontend_rules

    return base_rules

FLUTTER_COMPONENT_MAP = {
    "button/primary": "CustomButton",
    "button/secondary": "CustomButton.secondary",
    "card/default": "CustomCard",
    "appbar/mobile": "CustomAppBar",
    "search field": "SearchOverlay",
    "empty state": "CoreEmptyState",
    "loading": "GlobalOverlay",
    "snackbar": "CustomSnackbarAlert",
    "text field": "CustomTextField",
    "bottom sheet": "showModalBottomSheet",
    "tab bar": "CustomTabBar",
    "list item": "CustomListTile",
}

COMPANY_FLUTTER_RULES = [
    "Use CoreView<T> and CoreViewModel.",
    "Use repository pattern for API access.",
    "Do not call Dio directly from UI.",
    "Use GetIt for dependency injection.",
    "Use go_router for navigation.",
    "Use LangSingleton for localized labels.",
    "Use ThemeViewModel and theme.colorScheme for colors.",
    "Use GlobalOverlay for loading state.",
    "Use CustomSnackbarAlert for user feedback.",
    "Follow existing module structure under lib/modules when possible.",
    "Do not create new shared widgets if an existing core widget can be reused.",
    "Keep UI widgets small and split repeated sections into widgets.",
]

COMPONENT_MAPPINGS = {
    "Header/Dark": "CustomAppBar",
    "Search...": "CustomTextField",
    "Button": "CustomButton",
    "Leave Type Overview": "CustomCard",
    "Leave Request Rate": "CustomCard",
    "Employees Leave Balance": "CustomCard",
    "Leave Balance": "CustomTabBar",
    "Leave History": "CustomTabBar",
    "Leave Policy": "CustomTabBar",
    "Leave Details": "CustomTabBar",
}

def map_to_flutter_component(figma_name: str) -> str | None:
    normalized = figma_name.lower()

    for figma_component, flutter_component in FLUTTER_COMPONENT_MAP.items():
        if figma_component in normalized:
            return flutter_component

    return None