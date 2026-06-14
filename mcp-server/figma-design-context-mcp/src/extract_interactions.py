from extract_tokens import collect_nodes


def extract_interactions(root_node: dict) -> list[dict]:
    nodes = collect_nodes(root_node)
    interactions = []

    for node in nodes:
        name = str(node.get("name", ""))
        lowered = name.lower()

        if "search" in lowered:
            interactions.append(
                {
                    "trigger": "on_search",
                    "sourceNode": name,
                    "expectedBehavior": "Filter list data by keyword. Debounce if connected to API.",
                }
            )

        if "filter" in lowered:
            interactions.append(
                {
                    "trigger": "on_filter_tap",
                    "sourceNode": name,
                    "expectedBehavior": "Open filter bottom sheet or filter screen.",
                }
            )

        if "refresh" in lowered:
            interactions.append(
                {
                    "trigger": "on_pull_refresh",
                    "sourceNode": name,
                    "expectedBehavior": "Reload screen data from repository.",
                }
            )

        if "submit" in lowered or "save" in lowered:
            interactions.append(
                {
                    "trigger": "on_submit",
                    "sourceNode": name,
                    "expectedBehavior": "Validate input, call repository, show loading and feedback.",
                }
            )

        if "detail" in lowered or "card" in lowered or "item" in lowered:
            interactions.append(
                {
                    "trigger": "on_item_tap",
                    "sourceNode": name,
                    "expectedBehavior": "Navigate to detail screen if item is interactive.",
                }
            )

    return interactions