"""
This module provides functions to generate, validate, and update search modules using GPT-based responses.
It includes functionality to fetch and process HTML content, chunk HTML for processing, and handle exceptions
and retries.

Functions:
    generate_search_module(html_source: str, url: str) -> None:
        Generates a search module for extracting names from the given HTML source.

    validate_search_module(html_source: str, url: str) -> None:
        Validates the generated search module by extracting and validating names.

    _generate_code(source_chunks: list, gpt_chat: tuple) -> str:
        Generates code for the search module based on the HTML chunks.

    _update_code(original_code: str, error_message: str, html_chunk: str, names: list, gpt_chat: tuple) -> str:
        Updates the search module code based on error messages and additional HTML chunks.

    _save_module(code: str, url: str) -> None:
        Saves the generated or updated code to the appropriate file.

    _crop_code(code: str) -> str:
        Crops the generated code to extract the relevant function.

    _chunk_html(html: str, block_size: int) -> list:
        Chunks the HTML content into smaller blocks for processing.
"""

import os
import logging
import random

from .student_name import validate_names
from .search_module import search_names
from .gpt_api import get_gpt_response, init_gpt_chat
from .utils import parse_module_name, load_config, load_sys_path
from .exceptions import ValidationError, OpenAIError, ModuleError

load_sys_path()
_, NUM_ITERATIONS, _, SOURCE_CHUNK_LEN = load_config()


def generate_search_module(html_source: str, url: str) -> None:
    """
        Generates a search module for extracting names from the given HTML source.

        Args:
            html_source (str): The raw HTML content to generate the search module from.
            url (str): The URL of the page to generate the search module for.
        """
    gpt_chat = init_gpt_chat()

    html_chunks = _chunk_html(html_source, SOURCE_CHUNK_LEN)
    generated_code = _generate_code(html_chunks, gpt_chat)
    _save_module(generated_code, url)
    logging.info(f"Generated name search module")

    iteration = 0
    while iteration < NUM_ITERATIONS:
        iteration += 1
        try:
            validate_search_module(html_source, url)
            break

        except (ValidationError, ModuleError) as error_message:

            html_chunks = _chunk_html(html_source, SOURCE_CHUNK_LEN)
            try:
                try:
                    names = search_names(html_source, url)
                except ModuleError:
                    names = []
                updated_code = _update_code(
                    generated_code,
                    error_message,
                    html_chunks[iteration] if iteration < len(html_chunks) else "",
                    names,
                    gpt_chat
                )
                _save_module(updated_code, url)
            except (ValidationError, ModuleError) as e:
                logging.error(e)
                continue

            logging.info(f"Updated search module")
    else:
        logging.info(f"Failed to generate module after {NUM_ITERATIONS} attempts")


def validate_search_module(html_source: str, url: str) -> bool:
    """
    Validates the generated search module by extracting and validating names.

    Args:
        html_source (str): The raw HTML content to validate the search module against.
        url (str): The URL of the page to validate the search module for.

    Raises:
        ModuleError: If the module file is not found.
        ValidationError: If validation fails.
    """
    _, filepath = parse_module_name(url)
    if os.path.exists(filepath):
        try:
            names = search_names(html_source, url)
            return validate_names(html_source, names)

        except (ValidationError, ModuleError) as e:
            logging.error(e)
            raise
    else:
        raise ModuleError.file_not_found(filepath)


def _generate_code(source_chunks: list, gpt_chat: tuple) -> str:
    """
    Generates code for the search module based on the HTML chunks.

    Args:
        source_chunks (list): List of HTML chunks to generate the code from.
        gpt_chat (tuple): Initialized GPT chat object.

    Returns:
        str: The generated code as a string.
    """
    combined_html_chunks = "\n".join(source_chunks)
    prompt = gpt_chat[1]['generate_function_prompt'].format(
        html_chunks=combined_html_chunks
    )

    try:
        response_content = get_gpt_response(gpt_chat, prompt)
        return _crop_code(response_content)
    except (ValidationError, ModuleError, OpenAIError) as e:
        logging.error(e)
        return ""


def _update_code(
    original_code: str,
    error_message: str,
    html_chunk: str,
    names: list,
    gpt_chat: tuple
) -> str:
    """
    Updates the search module code based on error messages and additional HTML chunks.

    Args:
        original_code (str): The original generated code.
        error_message (str): The error message from the previous validation attempt.
        html_chunk (str): Additional HTML chunk to use for the update.
        names (list): List of names found in the HTML.
        gpt_chat (tuple): Initialized GPT chat object.

    Returns:
        str: The updated code as a string.
    """
    client, prompts, history = gpt_chat
    prompt = prompts['update_function_prompt'].format(
        function_code=original_code,
        error_message=error_message,
        names=names,
        html_chunk=html_chunk
    )
    try:
        updated_code = get_gpt_response(gpt_chat, prompt)
        return _crop_code(updated_code)
    except (ValidationError, ModuleError, OpenAIError) as e:
        logging.error(e)
        return ""


def _save_module(code: str, url: str) -> None:
    """
    Saves the generated or updated code to the appropriate file.

    Args:
        code (str): The generated or updated code.
        url (str): The URL to determine the file path for saving.
    """
    module_name, filepath = parse_module_name(url)
    with open(filepath, "w") as f:
        f.write(str(code))


def _crop_code(code: str) -> str:
    """
    Crops the generated code to extract the relevant function.

    Args:
        code (str): The full generated code.

    Returns:
        str: The cropped function code.
    """
    start_idx = code.find("```python") + len("```python") + 1
    end_idx = code.find('\n', code.find("return", start_idx)) + 1
    function_code = code[start_idx:end_idx]
    return function_code


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
