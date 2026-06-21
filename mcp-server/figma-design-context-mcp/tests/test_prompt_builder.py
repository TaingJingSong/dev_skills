import unittest

from prompt_builder import build_design_implementation_prompt


class PromptBuilderTests(unittest.TestCase):
    def test_builds_paste_ready_prompt_with_safety_rules(self) -> None:
        prompt = build_design_implementation_prompt(
            figma_url="https://www.figma.com/design/abc/Test?node-id=1-2",
            task="Implement the order list screen.",
            target_stack="mobile",
            design_context={"screen": {"name": "Orders"}},
            interactions={"prototypeInteractions": [], "nameBasedHints": []},
            max_input_chars=1000,
        )

        self.assertTrue(prompt.startswith("# Design Implementation Task"))
        self.assertIn("\n## 1. Objective\n", prompt)
        self.assertNotIn("\n        ##", prompt)
        self.assertIn("Do not code immediately", prompt)
        self.assertIn("Do not invent endpoints", prompt)
        self.assertIn("accessibility", prompt)
        self.assertIn("Tests and validation run with exact results", prompt)

    def test_bounds_free_text_inputs(self) -> None:
        prompt = build_design_implementation_prompt(
            figma_url="https://www.figma.com/design/abc/Test",
            task="x" * 200,
            target_stack="frontend",
            design_context={},
            interactions={},
            max_input_chars=100,
        )

        self.assertIn("[Input truncated at 100 characters.]", prompt)


if __name__ == "__main__":
    unittest.main()
