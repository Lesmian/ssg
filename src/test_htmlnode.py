import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_return_empty_string_when_no_props(self):
        node = HTMLNode("p", "This is paragraph text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_return_valid_props_html(self):
        node = HTMLNode("a", "This is link text", props={"href": "https://google.com", "class": "link"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" class="link"')
    
    def test_to_html_raises_error(self):
        node = HTMLNode("span", "This is span text")
        self.assertRaises(NotImplementedError, node.to_html)

if __name__ == "__main__":
    unittest.main()