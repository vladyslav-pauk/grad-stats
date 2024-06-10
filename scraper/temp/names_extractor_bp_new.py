import os
import sys
import requests
import re
import importlib.util
from typing import List, Tuple
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

GENERIC_NAMES = {'Student', 'Ph.D.', 'philosophy', 'education'}


def _load_extractors(module_path: str):
    extractors = {}
    for filename in os.listdir(module_path):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module_spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_path, filename))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            for attr in dir(module):
                if attr.startswith("extract_"):
                    extractors[module_name] = getattr(module, attr)
    return extractors


module_path = os.path.join(os.path.dirname(__file__), 'parser_modules')
extractors = _load_extractors(module_path)


def extract_names(soup: BeautifulSoup, url: str) -> Tuple[List[str], str, str]:
    for module_name, extractor_func in extractors.items():
        if all(substring in url for substring in module_name.split("_")):
            return extractor_func(soup), module_name.split("_")[1], module_name.split("_")[0]
    return [], '', ''


# Function to validate names against the HTML source
def validate_names(html_source: str, names: List[str]) -> bool:
    for name in names:
        name_pattern = re.compile(re.escape(name), re.IGNORECASE)
        if not name_pattern.search(html_source):
            return False
    return True


# Example usage
if __name__ == "__main__":
    with open('../urls.csv', 'r') as file:
        urls = [url.split(' ')[0] for url in file.readlines()]

    for url in urls:
        print("Processing URL:", url)
        html_source = requests.get(url).text
        names, university, department = extract_names(html_source, url)
        print("Extracted Names:", names)
        print("University:", university)
        print("Department:", department)
        is_valid = validate_names(html_source, names)
        print("Validation Result:", is_valid)