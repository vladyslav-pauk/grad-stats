"""
This module provides utility functions for loading configurations, managing system paths,
setting up logging, handling NLTK downloads, reading programs from CSV files, parsing module
names from URLs, and cleaning archived URLs.

Functions:
    load_config() -> tuple:
        Loads configuration settings from a JSON file.

    load_sys_path() -> None:
        Adds the project root to the system path.

    load_logging() -> None:
        Sets up logging configuration for the application.

    load_nltk() -> None:
        Downloads necessary NLTK data files.

    read_programs(filename: str) -> list:
        Reads program URLs from a CSV file and returns them as a list of tuples.

    parse_module_name(url: str) -> tuple:
        Parses the module name and filepath from a given URL.

    parent_url(url: str) -> str:
        Cleans an archived URL to its original form.
"""

import os
import csv
import re
import json
import sys
import random
import logging

from .exceptions import handle_exception


def load_config() -> tuple:
    """
    Loads configuration settings from a JSON file.

    Returns:
        tuple: A tuple containing configuration settings for MODEL, NUM_ITERATIONS, MAX_HISTORY_LEN, and SOURCE_CHUNK_LEN.
    """
    with open('scraper/src/config.json', 'r') as file:
        config = json.load(file)

    MODEL = config["MODEL"]
    NUM_ITERATIONS = config["NUM_ITERATIONS"]
    MAX_HISTORY_LEN = config["MAX_HISTORY_LEN"]
    SOURCE_CHUNK_LEN = config["SOURCE_CHUNK_LEN"]

    return MODEL, NUM_ITERATIONS, MAX_HISTORY_LEN, SOURCE_CHUNK_LEN


def load_sys_path() -> None:
    """
    Adds the project root to the system path.

    This function inserts the project root directory into the system path to enable absolute imports.
    """
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def load_logging(level='INFO') -> None:
    """
    Sets up logging configuration for the application.

    This function configures the logging settings, including the log format and log levels for different libraries.
    It also sets a custom exception handler for unhandled exceptions.
    """
    with open('scraper/src/config.json', 'r') as file:
        config = json.load(file)
    level = config['LOG_LEVEL']
    sys.excepthook = handle_exception
    logging.basicConfig(level=logging.getLevelName(level), format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger('nltk').setLevel(logging.ERROR)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)


def load_nltk() -> None:
    """
    Downloads necessary NLTK data files.

    This function downloads the required NLTK data files to a specified directory.
    """
    import nltk
    nltk_dir = "/Users/home/Work/Projects/phd-stats/venv/nltk_data"
    nltk.download('punkt', download_dir=nltk_dir, quiet=True)
    nltk.download('averaged_perceptron_tagger', download_dir=nltk_dir, quiet=True)
    nltk.download('maxent_ne_chunker', download_dir=nltk_dir, quiet=True)
    nltk.download('words', download_dir=nltk_dir, quiet=True)


def read_programs(filename: str) -> list:
    """
    Reads program URLs from a CSV file and returns them as a list of tuples.

    Args:
        filename (str): The name of the CSV file containing program URLs.

    Returns:
        list: A list of tuples where each tuple contains program URL details.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        url_tuples = [tuple(row) for row in reader]
    return url_tuples


def parse_module_name(url: str) -> tuple:
    """
    Parses the module name and filepath from a given URL.

    Args:
        url (str): The URL to parse.

    Returns:
        tuple: A tuple containing the module name and filepath.
    """
    pattern = r"(http).*(http)"
    replacement = r"\2"
    url = re.sub(pattern, replacement, url)
    url_parts = url.replace("https://", "").replace("http://", "").split(":")[0].split("/")[0].split(".")
    first_subdomain, second_subdomain = url_parts[:2]
    filename = f"{first_subdomain}_{second_subdomain}.py"
    directory = "scraper/src/search_modules"
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    return filename[:-3], filepath


def parent_url(url: str) -> str:
    """
    Cleans the archived URL to its original form.

    Args:
        url (str): The URL to be cleaned, typically from the web archive.

    Returns:
        str: The original URL if extractable, otherwise the input URL.
    """
    url_pattern = re.compile(r'https?://web\.archive\.org/web/\d+/(https?://.+)')
    match = url_pattern.search(url)
    url_match = match.group(1) if match else url
    url_match = url_match.replace(':80', '').replace('http://', 'https://')
    if url_match.endswith('/'):
        url_match = url_match[:-1]
    return url_match


def _chunk_html(html: str, block_size: int) -> list:
    """
    Chunks the HTML content into smaller blocks for processing.

    Args:
        html (str): The raw HTML content to chunk.
        block_size (int): The size of each chunk.

    Returns:
        list: A list of HTML chunks.
    """
    chunks = []
    for i in range(0, len(html), block_size):
        chunks.append(html[i:i + block_size])
    chunk_sample = random.sample(chunks, min(10, len(chunks)))
    return chunk_sample