def collect_nodes(node: dict, result: list[dict] | None = None) -> list[dict]:
    if result is None:
        result = []

    if not node:
        return result

    result.append(node)

    for child in node.get("children", []):
        collect_nodes(child, result)

    return result


def rgb_to_hex(color: dict | None) -> str | None:
    if not color:
        return None

    r = round(color.get("r", 0) * 255)
    g = round(color.get("g", 0) * 255)
    b = round(color.get("b", 0) * 255)

    return f"#{r:02X}{g:02X}{b:02X}"


def extract_design_tokens(root_node: dict) -> dict:
    nodes = collect_nodes(root_node)

    colors = set()
    spacing = set()
    radius = set()
    typography = set()

    for node in nodes:
        for fill in node.get("fills", []) or []:
            if fill.get("type") == "SOLID":
                hex_color = rgb_to_hex(fill.get("color"))
                if hex_color:
                    colors.add(hex_color)

        for key in [
            "itemSpacing",
            "paddingLeft",
            "paddingRight",
            "paddingTop",
            "paddingBottom",
        ]:
            value = node.get(key)
            if isinstance(value, (int, float)):
                spacing.add(value)

        corner_radius = node.get("cornerRadius")
        if isinstance(corner_radius, (int, float)):
            radius.add(corner_radius)

        if node.get("type") == "TEXT":
            style = node.get("style", {})
            typography.add(
                f"{style.get('fontFamily', 'Unknown')} / "
                f"{style.get('fontSize', 'Unknown')} / "
                f"{style.get('fontWeight', 'Unknown')}"
            )

    return {
        "colors": sorted(colors),
        "spacingCandidates": sorted(spacing),
        "radiusCandidates": sorted(radius),
        "typography": sorted(typography),
    }