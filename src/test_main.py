import unittest

from main import markdown_to_blocks, text_node_to_html_node, text_to_textnodes
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

    def test_text_to_textnodes_return_single_node_for_just_text(self):
        result = text_to_textnodes("This is just text")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is just text")

    def test_text_to_textnodes_parses_text_with_multiple_markdown_sections(self):
        result = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " with an ")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, " word and a ")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[5].text, "code block")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[6].text, " and an ")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].text, "obi wan image")
        self.assertEqual(result[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[8].text, " and a ")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].url, "https://boot.dev")

    def test_markdown_to_blocks_returns_single_block_for_one_line_text(self):
        result = markdown_to_blocks("# This is a heading")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "# This is a heading")

    def test_markdown_to_blocks_trims_empty_lines_and_whitespaces(self):
        result = markdown_to_blocks("# This is a heading\n\n\n\n   This is a paragraph of text.   ")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "# This is a heading")
        self.assertEqual(result[1], "This is a paragraph of text.")

if __name__ == "__main__":
    unittest.main()