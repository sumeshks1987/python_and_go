import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        txt = (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![logo](http://example.org/logo.svg)"
        )
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("logo", "http://example.org/logo.svg")
        ]
        self.assertEqual(expected, extract_markdown_images(txt))

    def test_extract_markdown_links(self):
        txt = (
            "Visit the [Python site](https://python.org) or "
            "check out the [Docs](/docs)."
        )
        expected = [
            ("Python site", "https://python.org"),
            ("Docs", "/docs")
        ]
        self.assertEqual(expected, extract_markdown_links(txt))

    def test_no_matches(self):
        txt = "Just plain text without any markdown."
        self.assertEqual([], extract_markdown_images(txt))
        self.assertEqual([], extract_markdown_links(txt))


if __name__ == "__main__":
    unittest.main()
