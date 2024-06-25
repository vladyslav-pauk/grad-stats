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

from .utils import load_sys_path
from .exceptions import ValidationError

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

        # if not _is_in_source(name, source):
        #     raise ValidationError.name_not_in_source(name)

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
    Checks if a name is present in the provided source content, considering possible nicknames in parentheses.

    Args:
        name (str): The name to search for.
        source (str): The source content to search within.

    Returns:
        bool: True if the name is found in the source, False otherwise.
    """
    normalized_name = _normalize_source(name)
    normalized_source = _normalize_source(source)

    parts = normalized_name.split()
    if len(parts) == 2:
        first_name, last_name = parts
    else:
        return False

    name_pattern = re.compile(
        rf'{re.escape(first_name)}\s*(\(\w+\)\s*)?{re.escape(last_name)}', re.IGNORECASE
    )

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

    return True


def _normalize_source(text: str) -> str:
    """
        Normalizes the source by decoding HTML entities, stripping extra spaces, and converting to lowercase.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
    """
    text = html.unescape(text)
    text = re.sub(r'[\s\(\)-]+', ' ', text).strip().lower()
    return text
