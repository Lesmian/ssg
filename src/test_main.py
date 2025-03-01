import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title_raises_error_if_no_title(self):
        self.assertRaisesRegex(Exception, "Markdown doesn't contain title", extract_title, "Some text")

    def test_extract_title_return_correct_text_for_single_line_markdown(self):
        result = extract_title("#   Hello   ")
        self.assertEqual(result, "Hello")

    def test_extract_title_return_correct_text_for_multiline_markdown(self):
        result = extract_title("# Hello\nsdfssd sdf \n sadfsd")
        self.assertEqual(result, "Hello")

if __name__ == "__main__":
    unittest.main()