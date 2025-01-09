import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links, split_nodes_delimiter


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

    def test_extract_markdown_images_return_empty_list_when_no_img_in_text(self):
        text = "This is text with no img"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 0)

    def test_extract_markdown_images_works_for_single_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) img"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "rick roll")
        self.assertEqual(result[0][1], "https://i.imgur.com/aKaOqIh.gif")

    def test_extract_markdown_images_works_for_multiple_imgs(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "rick roll")
        self.assertEqual(result[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[1][0], "obi wan")
        self.assertEqual(result[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links_return_empty_list_when_no_link_in_text(self):
        text = "This is text with no link"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 0)

    def test_extract_markdown_links_works_for_single_img(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)!"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "to boot dev")
        self.assertEqual(result[0][1], "https://www.boot.dev")

    def test_extract_markdown_links_works_for_multiple_imgs(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "to boot dev")
        self.assertEqual(result[0][1], "https://www.boot.dev")
        self.assertEqual(result[1][0], "to youtube")
        self.assertEqual(result[1][1], "https://www.youtube.com/@bootdotdev")


if __name__ == "__main__":
    unittest.main()