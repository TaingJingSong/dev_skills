from company_rules import COMPANY_FLUTTER_RULES, map_to_flutter_component
from extract_tokens import collect_nodes, extract_design_tokens


def to_widget_name(name: str) -> str:
    cleaned = "".join(char if char.isalnum() else " " for char in name)
    parts = [part.capitalize() for part in cleaned.split() if part]
    return "".join(parts) + "Widget"


def simplify_node(node: dict) -> dict:
    absolute_box = node.get("absoluteBoundingBox")

    return {
        "id": node.get("id"),
        "name": node.get("name"),
        "type": node.get("type"),
        "layoutMode": node.get("layoutMode"),
        "itemSpacing": node.get("itemSpacing"),
        "padding": {
            "left": node.get("paddingLeft"),
            "right": node.get("paddingRight"),
            "top": node.get("paddingTop"),
            "bottom": node.get("paddingBottom"),
        },
        "size": {
            "width": absolute_box.get("width"),
            "height": absolute_box.get("height"),
        }
        if absolute_box
        else None,
        "mappedFlutterComponent": map_to_flutter_component(node.get("name", "")),
    }


def extract_text_labels(nodes: list[dict]) -> list[dict]:
    labels = []

    for node in nodes:
        if node.get("type") == "TEXT" and node.get("characters"):
            labels.append(
                {
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "text": node.get("characters"),
                    "suggestedUsage": "Use LangSingleton/localization if this is user-facing text.",
                }
            )

    return labels


def infer_sections(root_node: dict) -> list[dict]:
    sections = []

    for child in root_node.get("children", []) or []:
        name = child.get("name", "")

        sections.append(
            {
                "id": child.get("id"),
                "name": name,
                "type": child.get("type"),
                "suggestedWidgetName": to_widget_name(name),
                "mappedFlutterComponent": map_to_flutter_component(name),
            }
        )

    return sections


def infer_layout(root_node: dict, platform: str) -> dict:
    absolute_box = root_node.get("absoluteBoundingBox", {})

    return {
        "screenSize": {
            "width": absolute_box.get("width"),
            "height": absolute_box.get("height"),
        },
        "likelyRootWidget": (
            "Scaffold + SafeArea + CustomScrollView/ListView"
            if platform == "mobile"
            else "Responsive page layout"
        ),
        "layoutMode": root_node.get("layoutMode", "UNKNOWN"),
        "recommendation": (
            "Use vertical scroll if content height can exceed viewport. "
            "Split cards, filters, lists, and summary sections into small widgets."
            if platform == "mobile"
            else "Use responsive constraints and avoid fixed-width layout."
        ),
    }


def extract_design_context(
    root_node: dict,
    platform: str = "mobile",
    framework: str = "flutter",
) -> dict:
    nodes = collect_nodes(root_node)
    simplified_nodes = [simplify_node(node) for node in nodes]

    component_matches = [
        {
            "figmaNode": node["name"],
            "figmaType": node["type"],
            "mappedComponent": node["mappedFlutterComponent"],
        }
        for node in simplified_nodes
        if node.get("mappedFlutterComponent")
    ]

    return {
        "screen": {
            "id": root_node.get("id"),
            "name": root_node.get("name"),
            "platform": platform,
            "framework": framework,
        },
        "layout": infer_layout(root_node, platform),
        "sections": infer_sections(root_node),
        "textLabels": extract_text_labels(nodes),
        "componentMatches": component_matches,
        "designTokens": extract_design_tokens(root_node),
        "implementationRules": COMPANY_FLUTTER_RULES if framework == "flutter" else [],
        "rawSummary": {
            "totalNodes": len(nodes),
            "nodeTypes": sorted({node.get("type") for node in nodes if node.get("type")}),
        },
    }