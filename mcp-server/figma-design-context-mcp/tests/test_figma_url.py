import unittest

from figma_url import parse_figma_url


class ParseFigmaUrlTests(unittest.TestCase):
    def test_parses_selected_node(self) -> None:
        parsed = parse_figma_url(
            "https://www.figma.com/design/AbC_123/File?node-id=12-34"
        )

        self.assertEqual(parsed.file_key, "AbC_123")
        self.assertEqual(parsed.node_id, "12:34")

    def test_rejects_non_figma_host(self) -> None:
        with self.assertRaisesRegex(ValueError, "Figma URL must use"):
            parse_figma_url(
                "https://example.com/design/AbC_123/File?node-id=12-34"
            )

    def test_rejects_invalid_node_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid Figma node-id"):
            parse_figma_url(
                "https://www.figma.com/design/AbC_123/File?node-id=not-a-node"
            )


if __name__ == "__main__":
    unittest.main()
