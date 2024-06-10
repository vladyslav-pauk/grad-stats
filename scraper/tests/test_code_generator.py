import unittest
from unittest.mock import patch
from scraper.src.code_generator import (
    _chunk_html,
    _crop_code,
    generate_name_search_function,
    execute_name_search_function,
    _update_code,
    validate_names_with_gpt,
    _extract_filepath
)
from scraper.tests.mock_openai import MockOpenAI


class TestNameExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://philosophy.princeton.edu/people/graduate-students"
        with open('scraper/src/tests/test_page.html', 'r') as file:
            cls.html = file.read()
        cls.chunks = _chunk_html(cls.html)
        cls.mock_client = MockOpenAI()

    def test_chunk_html(self):
        """Test that HTML is correctly split into chunks."""
        expected = self.html[:1000]
        self.assertEqual(_chunk_html(self.html, 1000)[0], expected)

    def test_extract_function_code(self):
        """Test that the function code is correctly extracted from the response."""
        code = "Here is the code\n\n```python\ndef extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n\nprint(extract_phd_student_names(html))\n```\n\nHere is the output."
        expected = "def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"
        self.assertEqual(_crop_code(code), expected)

    def test_generate_name_search_function(self):
        """Test that the name search function is correctly generated."""
        result = generate_name_search_function(self.chunks, self.mock_client)
        expected = "def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"
        self.assertEqual(result, expected)

    def test_save_name_search_function(self):
        """Test that the generated function code is correctly saved to a file."""
        code = "def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"
        filepath = _extract_filepath(self.url)
        with open(filepath, 'r') as f:
            saved_code = f.read()
        self.assertEqual(saved_code, code)

    @patch('scraper.src.code_generator.requests.get')
    def test_execute_name_search_function(self, mock_get):
        """Test that the generated function is correctly executed and returns the expected names."""
        mock_get.return_value.text = self.html
        # code = "def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"
        filepath = _extract_filepath(self.url)
        names = execute_name_search_function(self.url, filepath)
        self.assertEqual(names, ['Alice', 'Bob', 'Charlie'])

    def test_update_code_with_error(self):
        """Test that the generated function code is correctly updated with error information."""
        original_code = "def extract_phd_student_names(html: str) -> list[str]:\n    return []\n"
        error_message = "some error"
        names = ['Alice', 'Bob', 'Charlie']
        updated_code = _update_code(original_code, error_message, self.chunks, names, self.mock_client)
        expected = "def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"
        self.assertEqual(updated_code, expected)

    def test_validate_names_with_gpt(self):
        """Test that the names are correctly validated using GPT."""
        names = ['Alice', 'Bob', 'Charlie']
        result = validate_names_with_gpt(names, self.mock_client)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()