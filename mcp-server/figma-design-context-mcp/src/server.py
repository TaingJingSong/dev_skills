import json
from mcp.server.fastmcp import FastMCP

from figma_url import parse_figma_url
from figma_client import get_figma_file, get_figma_node
from extract_design_context import extract_design_context
from extract_tokens import extract_design_tokens
from extract_interactions import extract_interactions
from company_rules import FLUTTER_COMPONENT_MAP, get_stack_target, get_required_skills, get_rules_for_stack
from textwrap import dedent

mcp = FastMCP("figma-design-context-mcp")


async def get_root_node_from_figma_url(figma_url: str) -> dict:
    parsed = parse_figma_url(figma_url)

    if parsed.node_id:
        node_response = await get_figma_node(parsed.file_key, parsed.node_id)
        node_data = node_response.get("nodes", {}).get(parsed.node_id, {}).get("document")

        if not node_data:
            raise ValueError(f"Could not find Figma node: {parsed.node_id}")

        return node_data

    file_data = await get_figma_file(parsed.file_key)
    return file_data["document"]


@mcp.tool()
async def get_design_context(
    figma_url: str,
    platform: str = "mobile",
    framework: str = "flutter",
) -> str:
    """
    Extract implementation-ready design context from a Figma file or selected node.
    Use this before generating UI code.
    """
    root_node = await get_root_node_from_figma_url(figma_url)

    result = extract_design_context(
        root_node=root_node,
        platform=platform,
        framework=framework,
    )

    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def get_design_tokens(figma_url: str) -> str:
    """
    Extract colors, spacing, radius, and typography candidates from Figma.
    """
    root_node = await get_root_node_from_figma_url(figma_url)
    result = extract_design_tokens(root_node)

    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def get_screen_interactions(figma_url: str) -> str:
    """
    Infer possible UI interactions from Figma node names.
    """
    root_node = await get_root_node_from_figma_url(figma_url)

    result = {
        "screen": root_node.get("name"),
        "interactions": extract_interactions(root_node),
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def map_figma_to_project_components() -> str:
    """
    Return company Flutter component mappings.
    """
    result = {
        "framework": "flutter",
        "componentMap": FLUTTER_COMPONENT_MAP,
        "rules": [
            "Prefer mapped project components over creating new widgets.",
            "If no component mapping exists, return TODO instead of inventing a shared component.",
        ],
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def generate_design_based_prompt(
    figma_url: str,
    task: str,
    target_stack: str = "mobile",  # mobile | backend | frontend | fullstack
    project_root: str | None = None,
    existing_code_path: str | None = None,
    api_contract: str | None = None,
    business_rules: str | None = None,
    skill_names: list[str] | None = None,
):
    """
    Generate one skill-aware coding-agent prompt from Figma design context,
    project references, and company implementation rules.
    This does not generate code.
    """

    stack_target = get_stack_target(target_stack)
    platform = stack_target["platform"]
    framework = stack_target["framework"]

    required_skills = get_required_skills(target_stack, skill_names)
    implementation_rules = get_rules_for_stack(target_stack)

    root_node = await get_root_node_from_figma_url(figma_url)

    design_context = extract_design_context(
        root_node=root_node,
        platform=platform,
        framework=framework,
    )

    interactions = extract_interactions(root_node)

    prompt = dedent(f"""
    You are an AI coding agent working inside an existing company project.

    Your job is to implement the requested task using the provided Figma design context, existing project architecture, and available skills.

    ## Task

    {task}

    ## Target

    - Target stack: {target_stack}
    - Platform: {platform}
    - Framework: {framework}
    {f"- Project root: {project_root}" if project_root else "- Project root: Use the current workspace root."}
    {f"- Existing code reference: {existing_code_path}" if existing_code_path else "- Existing code reference: Inspect the project and identify the closest existing module."}

    ## Required Skills

    Before implementing, load and follow these skills if available:

    {chr(10).join(f"- {skill}" for skill in required_skills)}

    If any listed skill does not exist, do not stop. Continue by inspecting the current project and following discovered patterns.

    ## Mandatory Project Discovery

    Before editing files:

    1. Inspect the current project structure.
    2. Identify existing architecture patterns.
    3. Identify existing reusable widgets/components.
    4. Identify existing routing/navigation patterns.
    5. Identify existing model, repository, service, API, and state-management patterns.
    6. Verify whether suggested components exist before using them.
    7. Do not invent imports, components, models, API fields, or folder names.

    ## Figma Design Context

    {json.dumps(design_context, indent=2, ensure_ascii=False)}

    ## Inferred Interactions

    {json.dumps(interactions, indent=2, ensure_ascii=False)}

    ## API Contract

    {api_contract or "No API contract was provided. Inspect existing API/model/repository patterns. Do not invent request or response fields. Add TODO placeholders where API details are missing."}

    ## Business Rules

    {business_rules or "No business rules were provided. Do not invent approval, permission, validation, calculation, or workflow rules. Add TODOs where business behavior is unclear."}

    ## Implementation Rules

    {chr(10).join(f"- {rule}" for rule in implementation_rules)}

    ## Design Usage Rules

    - Treat Figma MCP component suggestions as hints only.
    - Verify all reusable components from the actual project before using them.
    - If a Figma section maps to no existing component, create a local private widget/component for this screen first.
    - Use design tokens as guidance, but prefer existing theme/design-system tokens if available.
    - Keep layout responsive and avoid fixed heights unless required.
    - Split repeated sections into small widgets/components.

    ## Required Output

    1. Summary of inspected files.
    2. Detected architecture and reusable patterns.
    3. Files created or modified.
    4. Implementation summary.
    5. Loading, empty, error, and success-state handling.
    6. TODOs for missing API contracts or business rules.
    7. Validation steps.

    ## Restrictions

    - Do not blindly use CustomButton, CustomCard, CoreView, CRUDAPI, or any named project component unless verified in the project.
    - Do not invent API request/response fields.
    - Do not bypass existing architecture.
    - Do not hardcode user-facing labels if localization exists.
    - Do not create duplicate shared widgets/components.
    - Do not modify unrelated files.
    """).strip()

    return prompt

if __name__ == "__main__":
    mcp.run()