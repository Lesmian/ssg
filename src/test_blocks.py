import unittest

from blocks import block_to_block_type, markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks_returns_single_block_for_one_line_text(self):
        result = markdown_to_blocks("# This is a heading")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "# This is a heading")

    def test_markdown_to_blocks_trims_empty_lines_and_whitespaces(self):
        result = markdown_to_blocks("# This is a heading\n\n\n\n   This is a paragraph of text.   ")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "# This is a heading")
        self.assertEqual(result[1], "This is a paragraph of text.")

    def test_markdown_to_blocks_keeps_multiline_blocks_together(self):
        result = markdown_to_blocks(">This is a quote\n>This is next line of same quote.")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ">This is a quote\n>This is next line of same quote.")

    def test_block_to_block_type_recognizes_paragraphs(self):
        result = block_to_block_type("This is just paragraph")
        self.assertEqual(result, "paragraph")
    
    def test_block_to_block_type_recognizes_heading_lvl1(self):
        result = block_to_block_type("# This is just heading")
        self.assertEqual(result, "heading")

    def test_block_to_block_type_recognizes_heading_lvl6(self):
        result = block_to_block_type("###### This is just heading")
        self.assertEqual(result, "heading")

    def test_block_to_block_type_recognizes_code(self):
        result = block_to_block_type("```This is just code\nsdfdsf\nwerewr\ndfgdfg```")
        self.assertEqual(result, "code")

    def test_block_to_block_type_recognizes_quote(self):
        result = block_to_block_type(">This is just code\n>sdfdsf\n>werewr\n>dfgdfg")
        self.assertEqual(result, "quote")

    def test_block_to_block_type__dont_recognizes_fake_quote(self):
        result = block_to_block_type(">This is just code\n>sdfdsf\nwerewr\n>dfgdfg")
        self.assertEqual(result, "paragraph")

    def test_block_to_block_type__dont_recognizes_unordered_list(self):
        result = block_to_block_type("* This is just code\n* sdfdsf\n- werewr\n- dfgdfg")
        self.assertEqual(result, "unordered_list")
    
    def test_block_to_block_type__dont_recognizes_fake_unordered_list(self):
        result = block_to_block_type("* This is just code\n*sdfdsf\n- werewr\n- dfgdfg")
        self.assertEqual(result, "paragraph")

    def test_block_to_block_type__dont_recognizes_ordered_list(self):
        result = block_to_block_type("1. This is just code\n2. sdfdsf\n3. werewr\n4. dfgdfg")
        self.assertEqual(result, "ordered_list")

    def test_block_to_block_type__dont_recognizes_ordered_list(self):
        result = block_to_block_type("1. This is just code\n3. sdfdsf\n3. werewr\n4. dfgdfg")
        self.assertEqual(result, "paragraph")

if __name__ == "__main__":
    unittest.main()