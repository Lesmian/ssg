import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node_raises_error_for_unknow_type(self):
        text = TextNode("test", "Weird")
        self.assertRaisesRegex(Exception, "Unknown text type", text_node_to_html_node, text)

    def test_text_node_to_html_node_converts_text(self):
        text = TextNode("This is just text", TextType.TEXT)
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), "This is just text")

    def test_text_node_to_html_node_converts_bold(self):
        text = TextNode("This is bold text", TextType.BOLD)
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), "<b>This is bold text</b>")

    def test_text_node_to_html_node_converts_italic(self):
        text = TextNode("This is italic text", TextType.ITALIC)
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), "<i>This is italic text</i>")

    def test_text_node_to_html_node_converts_code(self):
        text = TextNode("is_code = true", TextType.CODE)
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), "<code>is_code = true</code>")
    
    def test_text_node_to_html_node_converts_link(self):
        text = TextNode("This is link text", TextType.LINK, "https://google.com")
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), '<a href="https://google.com">This is link text</a>')

    def test_text_node_to_html_node_converts_image(self):
        text = TextNode("This is image text", TextType.IMAGE, "https://google.com/test.png")
        result = text_node_to_html_node(text)
        self.assertEqual(str(result), '<img src="https://google.com/test.png" alt="This is image text"></img>')

if __name__ == "__main__":
    unittest.main()