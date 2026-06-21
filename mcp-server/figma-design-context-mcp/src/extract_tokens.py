from typing import Any


def collect_nodes(root_node: dict[str, Any], max_nodes: int = 1500) -> tuple[list[dict], bool]:
    nodes: list[dict] = []
    stack = [root_node]

    while stack and len(nodes) < max_nodes:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        nodes.append(node)
        children = node.get("children", [])
        if isinstance(children, list):
            stack.extend(reversed(children))

    return nodes, bool(stack)


def rgb_to_hex(color: dict | None, opacity: float | None = None) -> str | None:
    if not color:
        return None

    channels = []
    for channel in ("r", "g", "b"):
        value = color.get(channel)
        if not isinstance(value, (int, float)):
            return None
        channels.append(max(0, min(255, round(value * 255))))

    alpha = opacity
    if alpha is None and isinstance(color.get("a"), (int, float)):
        alpha = color["a"]

    base = f"#{channels[0]:02X}{channels[1]:02X}{channels[2]:02X}"
    if isinstance(alpha, (int, float)) and alpha < 1:
        return f"{base}{max(0, min(255, round(alpha * 255))):02X}"
    return base


def extract_design_tokens(root_node: dict, max_nodes: int = 1500) -> dict:
    nodes, truncated = collect_nodes(root_node, max_nodes=max_nodes)
    colors: set[str] = set()
    spacing: set[float] = set()
    radius: set[float] = set()
    typography: set[tuple] = set()

    for node in nodes:
        for fill in node.get("fills", []) or []:
            if fill.get("type") == "SOLID" and fill.get("visible", True):
                color = rgb_to_hex(fill.get("color"), fill.get("opacity"))
                if color:
                    colors.add(color)

        for key in (
            "itemSpacing",
            "paddingLeft",
            "paddingRight",
            "paddingTop",
            "paddingBottom",
        ):
            value = node.get(key)
            if isinstance(value, (int, float)) and value >= 0:
                spacing.add(value)

        corner_radius = node.get("cornerRadius")
        if isinstance(corner_radius, (int, float)) and corner_radius >= 0:
            radius.add(corner_radius)

        if node.get("type") == "TEXT":
            style = node.get("style", {})
            typography.add(
                (
                    style.get("fontFamily"),
                    style.get("fontSize"),
                    style.get("fontWeight"),
                    style.get("lineHeightPx"),
                    style.get("textAlignHorizontal"),
                )
            )

    return {
        "colors": sorted(colors),
        "spacingCandidates": sorted(spacing),
        "radiusCandidates": sorted(radius),
        "typography": [
            {
                "fontFamily": value[0],
                "fontSize": value[1],
                "fontWeight": value[2],
                "lineHeight": value[3],
                "textAlign": value[4],
            }
            for value in sorted(typography, key=lambda item: str(item))
        ],
        "sourceNodeCount": len(nodes),
        "truncated": truncated,
    }
