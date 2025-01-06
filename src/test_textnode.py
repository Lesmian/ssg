import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is some url", TextType.LINK, "https://google.com")
        node2 = TextNode("This is some url", TextType.LINK, "https://google.com")
        self.assertEqual(node, node2)

    def test_missing_url_not_eq(self):
        node = TextNode("This is some url", TextType.LINK, "https://google.com")
        node2 = TextNode("This is some url", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_different_type_not_eq(self):
        node = TextNode("This is some text", TextType.LINK)
        node2 = TextNode("This is some text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    


if __name__ == "__main__":
    unittest.main()