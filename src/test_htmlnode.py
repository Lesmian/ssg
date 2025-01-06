import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_p_prints_correctly(self):
        node = HTMLNode("p", "This is paragraph text")
        self.assertEqual(str(node), "<p>This is paragraph text</p>")

    def test_link_prints_correctly(self):
        node = HTMLNode("a", "This is link text", props={"href": "https://google.com", "class": "link"})
        self.assertEqual(str(node), '<a href="https://google.com" class="link">This is link text</a>')
    
    def test_span_inside_div_prints_correctly(self):
        child_node = HTMLNode("span", "This is span text")
        parent_node = HTMLNode("div", children=child_node)
        self.assertEqual(str(parent_node), "<div><span>This is span text</span></div>")

if __name__ == "__main__":
    unittest.main()