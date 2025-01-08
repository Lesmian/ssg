import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter_raises_error_for_invalid_markdown(self):
        text = TextNode("This **is just text", TextType.TEXT)
        self.assertRaisesRegex(Exception, "Invalid markdown", split_nodes_delimiter, [text], "**", TextType.BOLD)

    def test_split_nodes_delimiter_handles_single_text_node(self):
        text = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_delimiter([text], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is just text")

    def test_split_nodes_delimiter_handles_node_with_single_bold_text(self):
        text = TextNode("This **is** just text", TextType.TEXT)
        result = split_nodes_delimiter([text], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This ")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "is")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " just text")

    def test_split_nodes_delimiter_handles_node_with_multiple_bold_texts(self):
        text = TextNode("This **is** just **text**", TextType.TEXT)
        result = split_nodes_delimiter([text], "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This ")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "is")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " just ")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "text")

    def test_split_nodes_delimiter_handles_node_with_just_italic_text(self):
        text = TextNode("*This is just text*", TextType.TEXT)
        result = split_nodes_delimiter([text], "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.ITALIC)
        self.assertEqual(result[0].text, "This is just text")

    def test_split_nodes_delimiter_handles_node_with_different_inline_elements(self):
        text = TextNode("This *is* just `text`", TextType.TEXT)
        result = split_nodes_delimiter([text], "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This ")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[1].text, "is")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " just `text`")


if __name__ == "__main__":
    unittest.main()