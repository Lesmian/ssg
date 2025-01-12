import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes


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

    def test_split_nodes_image_returns_text_if_no_img(self):
        text = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is just text")

    def test_split_nodes_image_returns_img_if_no_text(self):
        text = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].text, "rick roll")
        self.assertEqual(result[0].url, "https://i.imgur.com/aKaOqIh.gif")

    def test_split_nodes_image_returns_text_and_img_for_single_img(self):
        text = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) img", TextType.TEXT)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].text, "rick roll")
        self.assertEqual(result[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " img")

    def test_split_nodes_image_returns_text_and_img_for_multiple_img(self):
        text = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        result = split_nodes_image([text])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].text, "rick roll")
        self.assertEqual(result[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].text, "obi wan")
        self.assertEqual(result[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_split_nodes_link_returns_text_if_no_link(self):
        text = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is just text")

    def test_split_nodes_link_returns_link_if_no_text(self):
        text = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].text, "to boot dev")
        self.assertEqual(result[0].url, "https://www.boot.dev")

    def test_split_nodes_link_returns_text_and_link_for_single_link(self):
        text = TextNode("This is text with a link [to boot dev](https://www.boot.dev)!", TextType.TEXT)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is text with a link ")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].text, "to boot dev")
        self.assertEqual(result[1].url, "https://www.boot.dev")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "!")

    def test_split_nodes_link_returns_text_and_link_for_multiple_link(self):
        text = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        result = split_nodes_link([text])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].text, "This is text with a link ")
        self.assertEqual(result[1].text, "to boot dev")
        self.assertEqual(result[1].url, "https://www.boot.dev")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].text, "to youtube")
        self.assertEqual(result[3].url, "https://www.youtube.com/@bootdotdev")

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


if __name__ == "__main__":
    unittest.main()