import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_raises_error_if_no_tag(self):
        leafNode = LeafNode("p", "This is just paragraph text", {"id": "1"})
        parentNode = ParentNode(None, leafNode)
        self.assertRaisesRegex(ValueError, "Parent node must have a tag", parentNode.to_html)
    
    def test_to_html_raises_error_if_no_children(self):
        parentNode = ParentNode("div", None)
        self.assertRaisesRegex(ValueError, "Parent node must have children", parentNode.to_html)

    def test_to_html_return_valid_html_if_one_level_deep(self):
        leafNode = LeafNode("p", "This is just paragraph text", {"id": "1"})
        parentNode = ParentNode("div", [leafNode])
        self.assertEqual(parentNode.to_html(), '<div><p id="1">This is just paragraph text</p></div>')

    def test_to_html_return_valid_html_for_nested_parent_node(self):
        leafNode = LeafNode("span", "This is just text", {"class": "red"})
        parentNode = ParentNode("p", [leafNode])
        rootParentNode = ParentNode("div", [parentNode])
        self.assertEqual(rootParentNode.to_html(), '<div><p><span class="red">This is just text</span></p></div>')

    def test_to_html_return_valid_html_if_multiple_children(self):
        leafNode1 = LeafNode("p", "This is just paragraph text", {"id": "1"})
        leafNode2 = LeafNode("span", "This is just text")
        parentNode = ParentNode("div", [leafNode1, leafNode2])
        self.assertEqual(parentNode.to_html(), '<div><p id="1">This is just paragraph text</p><span>This is just text</span></div>')

if __name__ == "__main__":
    unittest.main()