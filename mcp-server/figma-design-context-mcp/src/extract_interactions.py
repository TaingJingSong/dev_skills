from extract_tokens import collect_nodes


def _prototype_interactions(node: dict) -> list[dict]:
    interactions = []
    for reaction in node.get("reactions", []) or []:
        if not isinstance(reaction, dict):
            continue
        interactions.append(
            {
                "sourceNodeId": node.get("id"),
                "sourceNode": node.get("name"),
                "evidence": "figma_prototype_reaction",
                "confidence": "high",
                "trigger": reaction.get("trigger"),
                "action": reaction.get("action"),
                "requiresConfirmation": False,
            }
        )
    return interactions


def _name_hint(node: dict) -> dict | None:
    name = str(node.get("name", ""))
    lowered = name.casefold()
    hints = (
        ("search", "search_input"),
        ("filter", "filter_control"),
        ("refresh", "refresh_control"),
        ("submit", "submit_action"),
        ("save", "save_action"),
    )

    for keyword, kind in hints:
        if keyword in lowered:
            return {
                "sourceNodeId": node.get("id"),
                "sourceNode": name,
                "evidence": f"node_name_contains:{keyword}",
                "confidence": "low",
                "interactionHint": kind,
                "requiresConfirmation": True,
            }
    return None


def extract_interactions(root_node: dict, max_nodes: int = 1500) -> dict:
    nodes, truncated = collect_nodes(root_node, max_nodes=max_nodes)
    prototype = []
    inferred = []
    seen_hints = set()

    for node in nodes:
        prototype.extend(_prototype_interactions(node))
        hint = _name_hint(node)
        if hint:
            key = (hint["sourceNodeId"], hint["interactionHint"])
            if key not in seen_hints:
                seen_hints.add(key)
                inferred.append(hint)

    return {
        "prototypeInteractions": prototype,
        "nameBasedHints": inferred,
        "warning": (
            "Name-based hints are not confirmed behavior. Verify them against prototype "
            "connections, requirements, and existing application behavior."
        ),
        "sourceNodeCount": len(nodes),
        "truncated": truncated,
    }
