import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_raises_error_if_no_value(self):
        node = LeafNode("p", None)
        self.assertRaisesRegex(ValueError, "Leaf node must have a value", node.to_html)

    def test_to_html_return_text_if_no_tag(self):
        node = LeafNode(None, "This is just raw text")
        self.assertEqual(node.to_html(), "This is just raw text")

    def test_to_html_return_valid_html(self):
        node = LeafNode("p", "This is just paragraph text", {"id": "1"})
        self.assertEqual(node.to_html(), '<p id="1">This is just paragraph text</p>')

if __name__ == "__main__":
    unittest.main()