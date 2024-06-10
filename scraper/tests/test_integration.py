import unittest
from unittest.mock import patch
from scraper.src.code_generator import (
    generate_function
)
from scraper.tests.mock_openai import MockOpenAI

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://philosophy.princeton.edu/people/graduate-students"
        with open('scraper/src/tests/test_page.html', 'r') as file:
            cls.html = file.read()
        cls.mock_client = MockOpenAI()

    def test_generated_function(self):
        """Test the entire generation and execution process for the name search function."""
        with patch('scraper.src.code_generator.requests.get') as mock_get:
            mock_get.return_value.text = self.html

            with patch('scraper.src.code_generator.generate_name_search_function',
                       return_value="def extract_phd_student_names(html: str) -> list[str]:\n    return ['Alice', 'Bob', 'Charlie']\n"):
                with patch('scraper.src.code_generator.validate_names_with_gpt', return_value=True):
                    generate_function(self.url, self.html, self.mock_client)


if __name__ == '__main__':
    unittest.main(verbosity=2)