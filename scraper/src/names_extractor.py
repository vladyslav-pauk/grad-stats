import os
import sys
import requests
import re
import importlib.util
import logging
from typing import List
from bs4 import BeautifulSoup
from .utils import init_gpt, extract_filepath

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

MODEL = "gpt-3.5-turbo"
client, _ = init_gpt()


def search_names(html_content: str, filepath: str) -> list:
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        [s.extract() for s in soup(['script', 'style'])]

        department, university = filepath.rsplit('/', 1)[-1].split('_')[:2]
        university = university.split('.')[0]
        module_name = f"{department}_{university}"

        try:
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            logging.error(f"Error loading module {module_name} when searching: {e}")
            return None
        names = module.extract_phd_student_names(soup)
        return names
    except Exception as e:
        logging.error("Name search module error:", e)
        return None


def validate_names(source: str, name_list: List[str]) -> bool:
    if len(name_list) == 0:
        logging.error("The extracted list is empty.")
        return False
    for name in name_list:
        name_pattern = re.compile(re.escape(name), re.IGNORECASE)
        if not name_pattern.search(source):
            logging.error(f"The extracted list contains non-name item: {name}")
            return False
    return True


# def _load_extractors(path: str):
#     extractor_dict = {}
#
#     try:
#         for filename in os.listdir(path):
#             if filename.endswith(".py"):
#                 module_name = filename[:-3]
#                 module_spec = importlib.util.spec_from_file_location(module_name, os.path.join(path, filename))
#                 module = importlib.util.module_from_spec(module_spec)
#                 try:
#                     module_spec.loader.exec_module(module)
#                 except Exception as e:
#                     logging.error(f"Error loading module {module_name}: {e}")
#                     # module_spec.loader.exec_module(module)
#                     # sys.exit()
#
#                 for attr in dir(module):
#                     if attr.startswith("extract_"):
#                         extractor_dict[module_name] = getattr(module, attr)
#         return extractor_dict
#     except Exception as e:
#         logging.error("Error loading name search module.")
#         return {}
#
#
# module_path = os.path.join(os.path.dirname(__file__), 'parser_modules')
# extractors = _load_extractors(module_path)
# def extract_names(source: str, url: str) -> Tuple[List[str], str, str]:
#     for module_name, extractor_func in extractors.items():
#         if all(substring in url for substring in module_name.split("_")):
#             soup = BeautifulSoup(source, 'html.parser')
#             [s.extract() for s in soup(['script', 'style'])]
#             try:
#                 name_list = extractor_func(soup)
#                 return name_list, module_name.split("_")[1], module_name.split("_")[0]
#             except Exception as e:
#                 logging.error(f"Error extracting names from {url}: {e}")
#                 return [], '', ''
#     return [], '', ''

# def validate_names_with_gpt(names: list, client) -> bool:
#     try:
#         if len(names) == 0:
#             return False
#         # print(names)
#         prompt = prompts['validate_names_prompt'].format(names=str(names))
#         response = client.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model=MODEL,
#         )
#         validation_result = response.choices[0].message.content.strip().lower()
#         # print(validation_result)
#         return "all items are valid names" in validation_result
#     except Exception as e:
#         print("GPT error:", e)
#         return False

# def validate_names(html: str, names: list) -> bool:
#     soup = BeautifulSoup(html, 'html.parser')
#     all_names = set()
#     content_list_items = soup.find_all('div', class_='content-list-item-details')
#     for item in content_list_items:
#         name_span = item.find('span', class_='field--name-title')
#         if name_span:
#             all_names.add(name_span.text)
#     return all_names == set(names)


if __name__ == "__main__":
    with open('../urls.csv', 'r') as file:
        urls = [url.split(' ')[0] for url in file.readlines()]

    for url in urls:
        print("Processing URL:", url)
        html_source = requests.get(url).text
        filepath = extract_filepath(url)
        department, university = filepath.rsplit('/', 1)[-1].split('_')[:2]
        university = university.split('.')[0]

        names = search_names(html_source, filepath)
        print("Extracted Names:", names)
        print("University:", university)
        print("Department:", department)
        is_valid = validate_names(html_source, names)
        print("Validation Result:", is_valid)
