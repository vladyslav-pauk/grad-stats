"""
This module provides functions to initialize a GPT chat session and get responses from the GPT API.
It includes functionality to load configuration, handle exceptions, and manage chat history.

Functions:
    get_gpt_response(gpt_chat: tuple, prompt: str) -> str:
        Fetches the response from the GPT API for the given prompt.

    init_gpt_chat() -> tuple:
        Initializes the GPT chat session by loading the API key and setup prompts.
"""

import os
from dotenv import load_dotenv
import yaml

import openai
from openai import OpenAI

from .exceptions import OpenAIError
from .utils import load_config, load_logging


MODEL, _, MAX_HISTORY_LEN, _ = load_config()
load_logging()


def get_gpt_response(gpt_chat: tuple, prompt: str) -> str:
    """
    Fetches the response from the GPT API for the given prompt.

    This function sends a prompt to the GPT API and returns the response. It manages the chat history
    to include previous exchanges and ensures that the history does not exceed the maximum allowed length.

    Args:
        gpt_chat (tuple): Initialized GPT chat object containing the client, prompts, and chat history.
        prompt (str): The prompt to send to the GPT API.

    Returns:
        str: The response content from the GPT API.

    Raises:
        OpenAIError: If there is an error with the GPT API call, such as API errors, connection errors, or rate limits.
    """
    client, _, history = gpt_chat

    if len(history) > MAX_HISTORY_LEN:
        history = history[-0.5 * MAX_HISTORY_LEN:]

    try:
        history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=MODEL,
            messages=history
        )
        response_content = response.choices[0].message.content.strip()

        history.append({"role": "assistant", "content": response_content})

        return response_content
    except (openai.APIError, openai.APIConnectionError, openai.RateLimitError) as e:
        status_code = getattr(e, 'code', None)
        raise OpenAIError(status_code)


def init_gpt_chat() -> tuple:
    """
    Initializes the GPT chat session by loading the API key and setup prompts.

    This function reads the OpenAI API key from the environment variables using dotenv, loads the initial setup prompts
    from a YAML file, and prepares the initial chat history. It returns a tuple containing the API client, the loaded
    prompts, and the initial chat history.

    Returns:
        tuple: A tuple containing the initialized client, prompts, and chat history.

    Raises:
        OpenAIError: If the API key is not found in the environment variables.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIError.api_key_not_found()
    client = OpenAI(api_key=api_key)

    with open('scraper/src/prompts.yaml', 'r') as file:
        prompts = yaml.safe_load(file)
    chat_history = [{"role": "user", "content": prompts["setup_prompt"]}]
    return client, prompts, chat_history
