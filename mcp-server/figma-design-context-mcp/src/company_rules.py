SKILL_ROUTING = {
    "mobile": [
        "mobile-core-structure",
        "flutter-build-responsive-layout",
        "generate-implementation-prompt",
    ],
    "backend": [
        "fastapi-generate-core-structure",
        "generate-implementation-prompt",
    ],
    "frontend": [
        "frontend-core-structure",
        "generate-implementation-prompt",
    ],
    "fullstack": [
        "mobile-core-structure",
        "fastapi-generate-core-structure",
        "generate-implementation-prompt",
    ],
}


STACK_TARGETS = {
    "mobile": {"platform": "mobile", "framework": "flutter"},
    "backend": {"platform": "backend", "framework": "fastapi"},
    "frontend": {"platform": "web", "framework": "frontend"},
    "fullstack": {"platform": "fullstack", "framework": "mixed"},
}


COMPONENT_HINTS = {
    "button/primary": "primary button",
    "button/secondary": "secondary button",
    "appbar": "application bar or page header",
    "search field": "search input",
    "empty state": "empty-state component",
    "loading": "loading indicator or overlay",
    "snackbar": "transient feedback component",
    "text field": "text input",
    "bottom sheet": "bottom sheet or modal",
    "tab bar": "tab navigation",
    "list item": "list item component",
}


def get_required_skills(
    target_stack: str,
    skill_names: list[str] | None = None,
) -> list[str]:
    if skill_names:
        return list(dict.fromkeys(skill_names))
    return SKILL_ROUTING.get(target_stack, ["generate-implementation-prompt"])


def get_stack_target(target_stack: str) -> dict[str, str]:
    if target_stack not in STACK_TARGETS:
        supported = ", ".join(STACK_TARGETS)
        raise ValueError(f"Unsupported target_stack. Expected one of: {supported}.")
    return STACK_TARGETS[target_stack]


def get_rules_for_stack(target_stack: str) -> list[str]:
    base_rules = [
        "Inspect repository instructions and the current project before editing.",
        "Use the closest maintained implementation as a structural reference.",
        "Verify components, routes, models, services, and skills before using them.",
        "Prefer existing design-system tokens and components over new equivalents.",
        "Create a local component first when reuse is unproven.",
        "Do not invent API fields, business rules, permissions, or navigation behavior.",
    ]

    stack_rules = {
        "mobile": [
            "Follow the project's state, navigation, localization, theme, and data-access patterns.",
            "Handle loading, empty, error, success, retry, and narrow-layout behavior where relevant.",
        ],
        "backend": [
            "Follow existing router, schema, service, model, repository, dependency, and permission patterns.",
            "Treat visual context as supporting information only; backend behavior requires a confirmed contract.",
        ],
        "frontend": [
            "Follow existing routing, state, API-client, theme, localization, accessibility, and component patterns.",
            "Implement responsive behavior from project breakpoints or clearly stated assumptions.",
        ],
        "fullstack": [
            "Separate UI, API, and data-contract assumptions and do not let the design define backend fields.",
            "Validate the complete loading, error, empty, success, permission, and retry flow.",
        ],
    }

    return base_rules + stack_rules[target_stack]


def map_component_hint(figma_name: str) -> str | None:
    normalized = figma_name.casefold()
    for figma_hint, component_kind in COMPONENT_HINTS.items():
        if figma_hint in normalized:
            return component_kind
    return None
