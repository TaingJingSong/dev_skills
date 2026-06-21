import json
from textwrap import dedent

from company_rules import get_required_skills, get_rules_for_stack, get_stack_target


def _bounded(value: str | None, limit: int, fallback: str) -> str:
    if not value or not value.strip():
        return fallback

    cleaned = value.strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}\n\n[Input truncated at {limit} characters.]"


def build_design_implementation_prompt(
    *,
    figma_url: str,
    task: str,
    target_stack: str,
    design_context: dict,
    interactions: dict,
    max_input_chars: int,
    project_root: str | None = None,
    existing_code_path: str | None = None,
    api_contract: str | None = None,
    business_rules: str | None = None,
    skill_names: list[str] | None = None,
) -> str:
    stack_target = get_stack_target(target_stack)
    required_skills = get_required_skills(target_stack, skill_names)
    implementation_rules = get_rules_for_stack(target_stack)

    task_text = _bounded(task, max_input_chars, "No task description was provided.")
    api_text = _bounded(
        api_contract,
        max_input_chars,
        "Not provided. Do not invent endpoints, methods, payloads, response fields, "
        "status behavior, or error contracts.",
    )
    rules_text = _bounded(
        business_rules,
        max_input_chars,
        "Not provided. Do not invent workflow, permission, validation, calculation, "
        "or approval rules.",
    )
    design_json = json.dumps(design_context, indent=2, ensure_ascii=False)
    interaction_json = json.dumps(interactions, indent=2, ensure_ascii=False)

    template = dedent(
        """
        # Design Implementation Task

        Implement the requested interface in the existing project using the Figma
        context below as the visual source of truth. Do not code immediately.

        ## 1. Objective

        {task}

        ## 2. Target

        - Stack: {target_stack}
        - Platform: {platform}
        - Framework: {framework}
        - Figma source: {figma_url}
        - Project root: {project_root}
        - Existing code reference: {existing_code_path}

        ## 3. Required Discovery

        Before editing:

        1. Read repository instructions.
        2. Inspect the project architecture, design system, theme, localization,
           navigation, state management, data access, and test patterns.
        3. Identify one or two maintained screens or modules with similar structure.
        4. Verify every suggested component, route, model, service, and skill exists.
        5. Prepare a short implementation plan covering files, states, responsiveness,
           accessibility, risks, assumptions, and validation.
        6. Stop for clarification when a missing contract would require invented behavior.

        ## 4. Figma Context

        ```json
        {design_context}
        ```

        Interpretation rules:

        - Preserve hierarchy, spacing relationships, typography intent, content priority,
          and visual grouping.
        - Treat frame dimensions as reference viewports, not fixed implementation sizes.
        - Prefer existing project tokens and components over raw Figma values.
        - Component hints are categories only and must be verified in the repository.
        - Do not derive backend fields, permissions, or business rules from visuals.
        - If the extract is truncated, inspect the Figma source or request narrower nodes.

        ## 5. Interaction Evidence

        ```json
        {interactions}
        ```

        Prototype reactions are confirmed design evidence. Name-based hints are
        hypotheses only; verify them against requirements and existing behavior.

        ## 6. Confirmed Contracts

        ### API Contract

        {api_contract}

        ### Business Rules

        {business_rules}

        ## 7. Relevant Skills

        Use these skills when installed and relevant:

        {required_skills}

        Do not stop solely because a suggested skill is unavailable. Continue using
        repository evidence and state which skill was unavailable.

        ## 8. Implementation Rules

        {implementation_rules}
        - Implement loading, empty, error, retry, success, disabled, and permission
          states when they are relevant and supported by requirements.
        - Preserve accessibility semantics, keyboard or focus behavior, readable
          contrast, dynamic text, and touch-target expectations for the platform.
        - Use responsive constraints and project breakpoints; avoid unexplained fixed
          dimensions.
        - Keep changes local. Promote a component to shared scope only when reuse is
          demonstrated.
        - Avoid unrelated refactors, dependencies, formatting churn, and generated-file edits.

        ## 9. Missing Information Policy

        - Blocking: API fields, database fields, permissions, business rules,
          navigation outcomes, or required visual states that cannot be derived safely.
        - Non-blocking: implementation details that can follow an established project pattern.
        - Use concise TODOs only for non-blocking gaps.
        - Never present assumptions or name-based interaction hints as confirmed facts.

        ## 10. Required Delivery

        Return:

        1. Project patterns and analogous modules inspected.
        2. Implementation plan.
        3. Files changed.
        4. Design fidelity and responsive behavior implemented.
        5. Loading, empty, error, retry, success, and accessibility handling.
        6. Tests and validation run with exact results.
        7. Remaining blocking questions, assumptions, and TODOs.
        """
    ).strip()

    return template.format(
        task=task_text,
        target_stack=target_stack,
        platform=stack_target["platform"],
        framework=stack_target["framework"],
        figma_url=figma_url,
        project_root=project_root or "Use the current workspace root.",
        existing_code_path=existing_code_path
        or "Find the closest maintained analogue in the repository.",
        design_context=design_json,
        interactions=interaction_json,
        api_contract=api_text,
        business_rules=rules_text,
        required_skills="\n".join(f"- {skill}" for skill in required_skills),
        implementation_rules="\n".join(
            f"- {rule}" for rule in implementation_rules
        ),
    )
