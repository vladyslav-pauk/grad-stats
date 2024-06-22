"""
This module provides functions to validate a list of names against a provided source content.

The validation process includes:
1. Checking the format of each name.
2. Verifying the presence of each name in the source content.
3. Determining if each name is likely a student's name based on named entities.

Functions:
    validate_names(source: str, name_list: List[str]) -> bool:
        Validates a list of names against the provided source content.

    _is_valid_name(name: str) -> bool:
        Checks if a name is valid by ensuring it contains at least two words.

    _is_in_source(name: str, source: str) -> bool:
        Checks if a name is present in the provided source content.

    _is_student_name(name: str) -> bool:
        Determines if a given name is likely a student's name by analyzing its structure and named entities.

    _normalize_source(text: str) -> str:
        Normalizes the source by decoding HTML entities, stripping extra spaces, and converting to lowercase.
"""

import re
import html
from typing import List

from nltk import word_tokenize, pos_tag, ne_chunk

from .utils import load_nltk, load_logging, load_sys_path
from .exceptions import ValidationError

load_nltk()
load_logging()
load_sys_path()


def validate_names(source: str, name_list: List[str]) -> bool:
    """
    Validate a list of names against the provided source content.

    This function checks the following criteria for each name in the list:
    - The name format: Each name must contain at least two words.
    - Presence in source: Each name must be found within the provided source content.
    - Student name validation: Each name must be identified as a student's name based on named entities.

    Args:
        source (str): The raw HTML or text content to validate the names against.
        name_list (List[str]): A list of names to validate.

    Returns:
        bool: True if all names are valid. Raises a ValidationError if validation fails for any name.

    Raises:
        ValidationError: If the name list is empty or any name fails validation.
                         The error message indicates the specific validation that failed.
    """
    if not name_list:
        raise ValidationError.empty_list()

    # print("Validating names:", name_list)

    for name in name_list:
        if not _is_valid_name(name):
            raise ValidationError.invalid_name_format(name)

        if not _is_in_source(name, source):
            raise ValidationError.name_not_in_source(name)

        if not _is_student_name(name):
            raise ValidationError.invalid_student_name(name)

    return True


def _is_valid_name(name: str) -> bool:
    """
        Checks if a name is valid by ensuring it contains at least two words.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
    """
    return len(name.strip(' ').split(' ')) >= 2


def _is_in_source(name: str, source: str) -> bool:
    """
        Checks if a name is present in the provided source content.

        Args:
            name (str): The name to search for.
            source (str): The source content to search within.

        Returns:
            bool: True if the name is found in the source, False otherwise.
    """
    normalized_name = _normalize_source(name)
    normalized_source = _normalize_source(source)

    name_pattern = re.compile(re.escape(normalized_name), re.IGNORECASE)
    return name_pattern.search(normalized_source) is not None


def _is_student_name(name: str) -> bool:
    """
    Determines if a given name is likely a student's name by analyzing its structure and named entities.

    Args:
        name (str): The name to check.

    Returns:
        bool: True if the name is likely a student's name, False otherwise.
    """
    name = name.replace('-', ' ')

    if name.startswith('Dr.') or name.startswith('Prof.'):
        return False

    tokens = word_tokenize(name)
    pos_tags = pos_tag(tokens)

    pos_tag_counts = {'JJR': 0, 'NNP': 0, 'NNS': 0, 'JJ': 0, 'NN': 0, 'RB': 0, 'VB': 0, 'S': 0, 'JJS': 0, 'VBG': 0}
    for _, tag in pos_tags:
        if tag not in pos_tag_counts:
            pos_tag_counts[tag] = 0
        pos_tag_counts[tag] += 1

    # print("Named entities: ", ne_chunk(pos_tags, binary=False))
    if (
            (pos_tag_counts['JJR'] == 1 and pos_tag_counts['NN'] == 1)
            or all(tag == 'NNP' for _, tag in pos_tags)
            or (pos_tag_counts['NNP'] == 1 and (
            pos_tag_counts['NNS'] == 1
            or pos_tag_counts['JJ'] == 1
            or pos_tag_counts['RB'] == 1
            or pos_tag_counts['JJR'] == 1))
            or (pos_tag_counts['JJS'] == 1 and pos_tag_counts['VBG'] == 1)
    ):
        return True

    return False
    # if all(tag == 'NNP' for _, tag in pos_tags):
    #     return True
    # for chunk in named_entities:
    #     if hasattr(chunk, 'label') and chunk.label() in {'PERSON', 'GPE'}:
    #         return True
    # if (pos_tag_counts['JJR'] >= 1 or pos_tag_counts['NNP'] >= 1 or pos_tag_counts['NNS']) and (pos_tag_counts['JJ'] >= 1 or pos_tag_counts['NN'] >= 1 or pos_tag_counts['RB'] or pos_tag_counts['VB'] >= 1 or pos_tag_counts['S'] >= 1):
    #     return True


def _normalize_source(text: str) -> str:
    """
        Normalizes the source by decoding HTML entities, stripping extra spaces, and converting to lowercase.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
    """
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

# def validate_names_with_gpt(names: list) -> bool:
#     from .utils import init_gpt_chat
#     from .exceptions import OpenAIError
#
#     MODEL_V = "gpt-4-turbo"
#     client_v, prompts, _ = init_gpt_chat()
#     try:
#         if client_v is None:
#             raise OpenAIError.client_required()
#
#         # httpx_logger = logging.getLogger("httpx")
#         # httpx_logger.setLevel(logging.WARNING)
#         if len(names) == 0:
#             return False
#
#         prompt = prompts['validate_names_prompt'].format(names=str(names))
#         # print("Validation prompt:", prompt)
#         response = client_v.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model=MODEL_V,
#         )
#         validation_result = response.choices[0].message.content.strip().lower()
#         # print("Validation result:", validation_result)
#         if not "all items are valid names" in validation_result:
#             raise ValidationError(validation_result)
#     except Exception as e:
#         raise e

# def is_student_name(name: str) -> bool:
#     ner_tagger = load_stanford_ner()
#     if name.startswith('Dr.'):
#         return False
#
#     tokens = word_tokenize(name)
#     ner_tags = ner_tagger.tag(tokens)
#
#     print(ner_tags)  # Debugging line to see the NER tags
#
#     for tag in ner_tags:
#         if tag[1] == 'PERSON':
#             return True
#
#     # Additional heuristic: Check if all tokens are proper nouns (NNP)
#     pos_tags = pos_tag(tokens)
#     if all(tag == 'NNP' for word, tag in pos_tags):
#         return True
#
#     return False

# if __name__ == "__main__":
#     with open('../../public/urls.csv', 'r') as file:
#         urls = [url.split(' ')[0] for url in file.readlines()]
#
#     for url in urls:
#         print("Processing URL:", url)
#         html_source = requests.get(url).text
#         filepath = extract_filepath(url)
#         department, university = dep_uni_name(filepath)
#
#         names = search_names(html_source, filepath)
#         print("Extracted Names:", names)
#         print("University:", university)
#         print("Department:", department)
#         is_valid = validate_names(html_source, names)
#         print("Validation Result:", is_valid)
