from typing import Any

from company_rules import map_component_hint
from extract_tokens import collect_nodes, extract_design_tokens


def _size(node: dict) -> dict[str, float | None] | None:
    box = node.get("absoluteBoundingBox")
    if not isinstance(box, dict):
        return None
    return {"width": box.get("width"), "height": box.get("height")}


def _padding(node: dict) -> dict[str, float | None]:
    return {
        "left": node.get("paddingLeft"),
        "right": node.get("paddingRight"),
        "top": node.get("paddingTop"),
        "bottom": node.get("paddingBottom"),
    }


def _sections(root_node: dict, limit: int = 100) -> tuple[list[dict], bool]:
    sections = []
    for child in root_node.get("children", []) or []:
        if len(sections) >= limit:
            return sections, True
        name = str(child.get("name", ""))
        sections.append(
            {
                "id": child.get("id"),
                "name": name,
                "type": child.get("type"),
                "layoutMode": child.get("layoutMode"),
                "size": _size(child),
                "componentHint": map_component_hint(name),
                "componentHintVerified": False,
            }
        )
    return sections, False


def _text_labels(nodes: list[dict], max_text_labels: int) -> tuple[list[dict], bool]:
    labels = []
    for node in nodes:
        if node.get("type") != "TEXT" or not node.get("characters"):
            continue
        labels.append(
            {
                "id": node.get("id"),
                "name": node.get("name"),
                "text": str(node["characters"])[:500],
                "textTruncated": len(str(node["characters"])) > 500,
                "style": node.get("style", {}),
            }
        )
        if len(labels) >= max_text_labels:
            return labels, True
    return labels, False


def _layout(root_node: dict, platform: str) -> dict:
    return {
        "screenSize": _size(root_node),
        "layoutMode": root_node.get("layoutMode"),
        "primaryAxisSizingMode": root_node.get("primaryAxisSizingMode"),
        "counterAxisSizingMode": root_node.get("counterAxisSizingMode"),
        "itemSpacing": root_node.get("itemSpacing"),
        "padding": _padding(root_node),
        "platformGuidance": (
            "Treat the frame size as a reference viewport, not a fixed implementation size. "
            "Derive responsive behavior from project patterns and content constraints."
            if platform in {"mobile", "web", "fullstack"}
            else "Use visual context only as supporting information for non-UI work."
        ),
    }


def extract_design_context(
    root_node: dict[str, Any],
    platform: str = "mobile",
    framework: str = "flutter",
    max_nodes: int = 1500,
    max_text_labels: int = 250,
) -> dict:
    nodes, nodes_truncated = collect_nodes(root_node, max_nodes=max_nodes)
    text_labels, labels_truncated = _text_labels(nodes, max_text_labels)
    sections, sections_truncated = _sections(root_node)
    component_hints = []

    for node in nodes:
        if len(component_hints) >= 200:
            break
        hint = map_component_hint(str(node.get("name", "")))
        if hint:
            component_hints.append(
                {
                    "figmaNodeId": node.get("id"),
                    "figmaNode": node.get("name"),
                    "figmaType": node.get("type"),
                    "componentKindHint": hint,
                    "verifiedInProject": False,
                }
            )

    return {
        "screen": {
            "id": root_node.get("id"),
            "name": root_node.get("name"),
            "type": root_node.get("type"),
            "platform": platform,
            "framework": framework,
        },
        "layout": _layout(root_node, platform),
        "sections": sections,
        "textLabels": text_labels,
        "componentHints": component_hints,
        "designTokens": extract_design_tokens(root_node, max_nodes=max_nodes),
        "implementationGuidance": [
            "Verify every component hint against the target repository.",
            "Prefer project theme and design-system tokens over raw Figma values.",
            "Preserve semantic hierarchy, content priority, and interaction intent.",
            "Do not infer backend contracts, permissions, or business rules from visuals.",
        ],
        "sourceSummary": {
            "totalNodesIncluded": len(nodes),
            "nodeTypes": sorted(
                {node.get("type") for node in nodes if node.get("type")}
            ),
            "nodesTruncated": nodes_truncated,
            "sectionsTruncated": sections_truncated,
            "textLabelsTruncated": labels_truncated,
            "componentHintsTruncated": len(component_hints) >= 200,
        },
    }
