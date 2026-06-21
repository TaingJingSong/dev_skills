import unittest

from extract_design_context import extract_design_context
from extract_interactions import extract_interactions
from extract_tokens import rgb_to_hex


ROOT_NODE = {
    "id": "1:1",
    "name": "Orders",
    "type": "FRAME",
    "absoluteBoundingBox": {"width": 390, "height": 844},
    "children": [
        {
            "id": "1:2",
            "name": "Search field",
            "type": "FRAME",
            "reactions": [
                {
                    "trigger": {"type": "ON_CLICK"},
                    "action": {"type": "NODE", "destinationId": "2:1"},
                }
            ],
            "children": [
                {
                    "id": "1:3",
                    "name": "Label",
                    "type": "TEXT",
                    "characters": "Search orders",
                    "style": {"fontFamily": "Inter", "fontSize": 16},
                    "fills": [
                        {
                            "type": "SOLID",
                            "color": {"r": 1, "g": 0.5, "b": 0},
                        }
                    ],
                }
            ],
        }
    ],
}


class ExtractorTests(unittest.TestCase):
    def test_context_marks_component_hints_unverified(self) -> None:
        context = extract_design_context(ROOT_NODE)

        self.assertEqual(context["screen"]["name"], "Orders")
        self.assertFalse(context["componentHints"][0]["verifiedInProject"])
        self.assertEqual(context["textLabels"][0]["text"], "Search orders")

    def test_interactions_separate_evidence_from_hints(self) -> None:
        interactions = extract_interactions(ROOT_NODE)

        self.assertEqual(
            interactions["prototypeInteractions"][0]["confidence"],
            "high",
        )
        self.assertTrue(interactions["nameBasedHints"][0]["requiresConfirmation"])

    def test_reports_node_truncation(self) -> None:
        context = extract_design_context(ROOT_NODE, max_nodes=1)

        self.assertTrue(context["sourceSummary"]["nodesTruncated"])

    def test_color_includes_alpha_when_translucent(self) -> None:
        self.assertEqual(
            rgb_to_hex({"r": 1, "g": 0, "b": 0}, opacity=0.5),
            "#FF000080",
        )


if __name__ == "__main__":
    unittest.main()
