"""
This module provides functions to search for names in HTML content using dynamically loaded search modules.

Functions:
    search_names(html_content: str, url: str) -> List[str]:
        Searches for names in the provided HTML content using the appropriate search module.

    _parse_source(html_content: str) -> BeautifulSoup:
        Parses the HTML content and removes script and style elements.

    _load_module(url: str) -> types.ModuleType:
        Loads the search module based on the provided URL.

    _extract_names(module: types.ModuleType, soup: BeautifulSoup) -> List[str]:
        Extracts names using the provided module from the parsed HTML content.
"""

import importlib.util
import warnings
from typing import List
import types

from bs4 import BeautifulSoup


from .utils import parse_module_name, load_sys_path
from .exceptions import ModuleError


load_sys_path()


def search_names(html_content: str, url: str) -> list:
    """
    Searches for names in the provided HTML content.

    This function parses the raw HTML content to extract and return a list of names.
    The provided URL is used to load the appropriate search module.

    Args:
        html_content (str): The raw HTML content to search for names.
        url (str): The URL from which the HTML content was retrieved.

    Returns:
        List[str]: A list of names found within the HTML content.

    Raises:
        ModuleError: If there is an issue loading or executing the search module.
    """
    source = _parse_source(html_content)
    search_module = _load_module(url)
    names = _extract_names(search_module, source)
    return names


def _parse_source(html_content: str) -> BeautifulSoup:
    """
        Parses the HTML content and removes script and style elements.

        Args:
            html_content (str): The raw HTML content.

        Returns:
            BeautifulSoup: The parsed HTML content.
    """
    parsed_source = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in parsed_source(['script', 'style'])]
    return parsed_source


def _load_module(url: str) -> types.ModuleType:
    """
    Loads the search module based on the provided URL.

    Args:
        url (str): The URL used to determine the module to load.

    Returns:
        types.ModuleType: The loaded module.

    Raises:
        ModuleError: If there is an issue importing the module.
    """
    module_name, filepath = parse_module_name(url)
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)

        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            spec.loader.exec_module(module)

        return module
    except Exception:
        raise ModuleError.load_error()


def _extract_names(module: types.ModuleType, soup: BeautifulSoup) -> List[str]:
    """
    Extracts names using the provided module from the parsed HTML content.

    Args:
        module (types.ModuleType): The search module to use for extracting names.
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        List[str]: A list of names found within the HTML content.

    Raises:
        ModuleError: If there is an issue during the execution of the module.
    """
    try:
        names = module.extract_phd_student_names(soup)
        return [name.replace('\n', '').replace(r'\s+', ' ') for name in names if name]
    except Exception:
        raise ModuleError.execution_error()
