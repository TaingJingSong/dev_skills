from typing import Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from company_rules import COMPONENT_HINTS
from config import load_settings
from extract_design_context import extract_design_context
from extract_interactions import extract_interactions
from extract_tokens import extract_design_tokens
from figma_client import get_figma_file, get_figma_node
from figma_url import ParsedFigmaUrl, parse_figma_url
from prompt_builder import build_design_implementation_prompt


mcp = FastMCP(
    "figma-design-context-mcp",
    instructions=(
        "Extract bounded, evidence-based Figma context and produce paste-ready "
        "implementation prompts. Visual context never defines missing API, database, "
        "permission, or business contracts. Prefer get_design_context for inspection or "
        "generate_design_based_prompt for a coding prompt; do not call every extraction "
        "tool for the same URL because design context already includes tokens and interactions."
    ),
    json_response=True,
)


class DesignContextResult(BaseModel):
    source: dict[str, str | None]
    design_context: dict[str, Any]
    interactions: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)


class DesignPromptResult(BaseModel):
    prompt: str
    source: dict[str, str | None]
    warnings: list[str] = Field(default_factory=list)


async def get_root_node_from_figma_url(
    figma_url: str,
) -> tuple[ParsedFigmaUrl, dict[str, Any]]:
    parsed = parse_figma_url(figma_url)

    if parsed.node_id:
        response = await get_figma_node(parsed.file_key, parsed.node_id)
        node_data = response.get("nodes", {}).get(parsed.node_id, {}).get("document")
        if not isinstance(node_data, dict):
            raise ValueError(f"Figma node was not found: {parsed.node_id}")
        return parsed, node_data

    file_data = await get_figma_file(parsed.file_key)
    document = file_data.get("document")
    if not isinstance(document, dict):
        raise ValueError("Figma file response did not contain a document.")
    return parsed, document


def _source(parsed: ParsedFigmaUrl, root_node: dict) -> dict[str, str | None]:
    return {
        "fileKey": parsed.file_key,
        "nodeId": parsed.node_id,
        "nodeName": root_node.get("name"),
    }


def _warnings(design_context: dict, interactions: dict) -> list[str]:
    warnings = [
        "Component hints are unverified until matched against the target repository.",
        "Figma visuals do not define API, database, permission, or business contracts.",
    ]
    summary = design_context.get("sourceSummary", {})
    if any(
        summary.get(key)
        for key in (
            "nodesTruncated",
            "sectionsTruncated",
            "textLabelsTruncated",
            "componentHintsTruncated",
        )
    ):
        warnings.append(
            "The extracted context was truncated. Use a narrower Figma node for higher fidelity."
        )
    if interactions.get("nameBasedHints"):
        warnings.append(
            "Name-based interaction hints require confirmation from requirements or prototypes."
        )
    return warnings


async def _extract(
    figma_url: str,
    platform: str,
    framework: str,
) -> DesignContextResult:
    settings = load_settings()
    parsed, root_node = await get_root_node_from_figma_url(figma_url)
    design_context = extract_design_context(
        root_node,
        platform=platform,
        framework=framework,
        max_nodes=settings.max_nodes,
        max_text_labels=settings.max_text_labels,
    )
    interactions = extract_interactions(root_node, max_nodes=settings.max_nodes)
    return DesignContextResult(
        source=_source(parsed, root_node),
        design_context=design_context,
        interactions=interactions,
        warnings=_warnings(design_context, interactions),
    )


@mcp.tool(
    title="Get Figma design context",
    description=(
        "Extract bounded layout, text, tokens, component-category hints, and "
        "interaction evidence from a Figma file or selected node. This comprehensive "
        "result already includes tokens and interactions."
    ),
)
async def get_design_context(
    figma_url: str,
    platform: str = "mobile",
    framework: str = "flutter",
) -> DesignContextResult:
    return await _extract(figma_url, platform, framework)


@mcp.tool(
    title="Get Figma design tokens",
    description="Extract bounded color, spacing, radius, and typography candidates.",
)
async def get_design_tokens(figma_url: str) -> dict[str, Any]:
    settings = load_settings()
    parsed, root_node = await get_root_node_from_figma_url(figma_url)
    return {
        "source": _source(parsed, root_node),
        "tokens": extract_design_tokens(root_node, max_nodes=settings.max_nodes),
        "warning": "Prefer verified project design-system tokens over raw Figma values.",
    }


@mcp.tool(
    title="Get Figma interaction evidence",
    description=(
        "Return prototype reactions separately from low-confidence node-name hints. "
        "Use only when interaction evidence is needed without full design context."
    ),
)
async def get_screen_interactions(figma_url: str) -> dict[str, Any]:
    settings = load_settings()
    parsed, root_node = await get_root_node_from_figma_url(figma_url)
    return {
        "source": _source(parsed, root_node),
        "interactions": extract_interactions(root_node, max_nodes=settings.max_nodes),
    }


@mcp.tool(
    title="Get component mapping guidance",
    description=(
        "Return generic component-category hints that must be verified in the target project."
    ),
)
async def map_figma_to_project_components() -> dict[str, Any]:
    return {
        "componentHints": COMPONENT_HINTS,
        "rules": [
            "Treat mappings as categories, not real project component names.",
            "Verify the target repository before selecting or creating a component.",
            "Prefer a local component until shared reuse is demonstrated.",
        ],
    }


@mcp.tool(
    title="Generate design implementation prompt",
    description=(
        "Generate a paste-ready coding-agent prompt from Figma context and optional "
        "project, API, and business references. This tool does not generate code."
    ),
)
async def generate_design_based_prompt(
    figma_url: str,
    task: str,
    target_stack: str = "mobile",
    project_root: str | None = None,
    existing_code_path: str | None = None,
    api_contract: str | None = None,
    business_rules: str | None = None,
    skill_names: list[str] | None = None,
) -> DesignPromptResult:
    settings = load_settings()
    stack = {
        "mobile": ("mobile", "flutter"),
        "backend": ("backend", "fastapi"),
        "frontend": ("web", "frontend"),
        "fullstack": ("fullstack", "mixed"),
    }
    if target_stack not in stack:
        raise ValueError(
            "Unsupported target_stack. Expected mobile, backend, frontend, or fullstack."
        )

    extracted = await _extract(figma_url, *stack[target_stack])
    prompt = build_design_implementation_prompt(
        figma_url=figma_url,
        task=task,
        target_stack=target_stack,
        design_context=extracted.design_context,
        interactions=extracted.interactions,
        max_input_chars=settings.max_prompt_input_chars,
        project_root=project_root,
        existing_code_path=existing_code_path,
        api_contract=api_contract,
        business_rules=business_rules,
        skill_names=skill_names,
    )
    return DesignPromptResult(
        prompt=prompt,
        source=extracted.source,
        warnings=extracted.warnings,
    )


@mcp.prompt(
    name="design_from_figma",
    title="Design from Figma context",
    description="Create a paste-ready implementation prompt from a Figma URL and task.",
)
async def design_from_figma(
    figma_url: str,
    task: str,
    target_stack: str = "mobile",
) -> str:
    result = await generate_design_based_prompt(
        figma_url=figma_url,
        task=task,
        target_stack=target_stack,
    )
    return result.prompt


if __name__ == "__main__":
    mcp.run()
