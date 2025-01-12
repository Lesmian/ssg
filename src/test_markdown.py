import unittest

from blocks import block_to_block_type, markdown_to_blocks
from markdown import markdown_to_html_node


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_html_node_works_for_singe_paragraph(self):
        result = markdown_to_html_node("This is a paragraph")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].value, "This is a paragraph")

    def test_markdown_to_html_node_works_for_heading_lvl2(self):
        result = markdown_to_html_node("## This is a heading")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "h2")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].value, "This is a heading")

    def test_markdown_to_html_node_works_for_code(self):
        result = markdown_to_html_node("```Some code\nSecond line of code```")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].value, "Some code\nSecond line of code")

    def test_markdown_to_html_node_works_for_quote(self):
        result = markdown_to_html_node(">Some quote\n>Second line of quote")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "quote")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].value, "Some quote\nSecond line of quote")

    def test_markdown_to_html_node_works_for_unordered_list(self):
        result = markdown_to_html_node("* Some item\n- Another item")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(len(result.children[0].children), 2)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(len(result.children[0].children[0].children), 1)
        self.assertEqual(result.children[0].children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].children[0].value, "Some item")
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(len(result.children[0].children[1].children), 1)
        self.assertEqual(result.children[0].children[1].children[0].tag, None)
        self.assertEqual(result.children[0].children[1].children[0].value, "Another item")

    def test_markdown_to_html_node_works_for_ordered_list(self):
        result = markdown_to_html_node("1.First item\n2.Second item")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children), 2)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(len(result.children[0].children[0].children), 1)
        self.assertEqual(result.children[0].children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].children[0].value, "First item")
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(len(result.children[0].children[1].children), 1)
        self.assertEqual(result.children[0].children[1].children[0].tag, None)
        self.assertEqual(result.children[0].children[1].children[0].value, "Second item")

    def test_markdown_to_html_node_works_for_ordered_list_with_bold_text(self):
        result = markdown_to_html_node("1.First item with **bold** text\n2.Second item")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children), 2)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(len(result.children[0].children[0].children), 3)
        self.assertEqual(result.children[0].children[0].children[0].tag, None)
        self.assertEqual(result.children[0].children[0].children[0].value, "First item with ")
        self.assertEqual(result.children[0].children[0].children[1].tag, "b")
        self.assertEqual(result.children[0].children[0].children[1].value, "bold")
        self.assertEqual(result.children[0].children[0].children[2].tag, None)
        self.assertEqual(result.children[0].children[0].children[2].value, " text")
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(len(result.children[0].children[1].children), 1)
        self.assertEqual(result.children[0].children[1].children[0].value, "Second item")

if __name__ == "__main__":
    unittest.main()