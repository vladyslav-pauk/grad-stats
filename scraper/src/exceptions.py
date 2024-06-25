"""
This module defines custom exception classes for handling various types of errors and a function
for logging unhandled exceptions. It provides specialized exceptions for validation errors,
module-related errors, OpenAI API errors, and Wayback Machine errors.

Classes:
    ValidationError:
        Raised for validation-related errors.

    ModuleError:
        Raised when there is a module-related error.

    OpenAIError:
        Raised when there is an OpenAI API-related error.

    WaybackMachineError:
        Raised when an HTTP error occurs with the Wayback Machine.

Functions:
    handle_exception(exc_type, exc_value, exc_traceback):
        Logs unhandled exceptions, except for keyboard interrupts.
"""
import logging
import sys
import time
from typing import Type, Optional
from types import TracebackType

from requests.exceptions import ConnectionError, HTTPError, Timeout
from urllib3.exceptions import NewConnectionError


def handle_exception(exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: Optional[TracebackType]) -> None:
    """
    Logs unhandled exceptions, except for keyboard interrupts.

    Args:
        exc_type (Type[BaseException]): The exception type.
        exc_value (BaseException): The exception instance.
        exc_traceback (Optional[TracebackType]): The traceback object.

    Returns:
        None
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


def handle_retry_exception(exc: Exception, attempts: int, retry_delay: int) -> tuple[int, int]:
    logging.error(f"Retrying in {retry_delay}s - Wayback Machine connection failed")
    # logging.error(f"Retrying in {retry_delay}s - {exc}")
    time.sleep(retry_delay)
    retry_delay *= 2
    attempts += 1
    return retry_delay, attempts


class ValidationError(Exception):
    """
    Raised for validation-related errors.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message="Failed"):
        self.message = f"Validation: {message}"
        super().__init__(self.message)

    @classmethod
    def invalid_name_format(cls, name):
        """
        Creates a ValidationError for an invalid name format.

        Args:
            name (str): The invalid name.

        Returns:
            ValidationError: An instance of ValidationError.
        """
        return cls(f"'{name}' must be two words or longer")

    @classmethod
    def name_not_in_source(cls, name):
        """
        Creates a ValidationError for a name not found in the source.

        Args:
            name (str): The name not found in the source.

        Returns:
            ValidationError: An instance of ValidationError.
        """
        return cls(f"Item not in source: {name}")

    @classmethod
    def invalid_student_name(cls, name):
        """
        Creates a ValidationError for an invalid student name.

        Args:
            name (str): The invalid student name.

        Returns:
            ValidationError: An instance of ValidationError.
        """
        return cls(f"Invalid name: {name}")

    @classmethod
    def empty_list(cls):
        """
        Creates a ValidationError for an empty list.

        Returns:
            ValidationError: An instance of ValidationError.
        """
        return cls("Empty list")


class ModuleError(Exception):
    """
    Raised when there is a module-related error.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message="Failed"):
        self.message = f"Module: {message}"
        super().__init__(self.message)

    @classmethod
    def execution_error(cls):
        """
        Creates a ModuleError for execution failure.

        Returns:
            ModuleError: An instance of ModuleError.
        """
        return cls("Failed to execute")

    @classmethod
    def load_error(cls):
        """
        Creates a ModuleError for loading failure.

        Returns:
            ModuleError: An instance of ModuleError.
        """
        return cls("Failed to load")

    @classmethod
    def file_not_found(cls, filepath):
        """
        Creates a ModuleError for a file not found.

        Args:
            filepath (str): The path of the file not found.

        Returns:
            ModuleError: An instance of ModuleError.
        """
        return cls(f"{filepath} not found")


class OpenAIError(Exception):
    """
    Raised when there is an OpenAI API-related error.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message="Error"):
        self.message = f"OpenAI API: {message}"
        super().__init__(self.message)

    @classmethod
    def insufficient_balance(cls):
        """
        Creates an OpenAIError for insufficient balance.

        Returns:
            OpenAIError: An instance of OpenAIError.
        """
        return cls("Insufficient balance")

    @classmethod
    def client_required(cls):
        """
        Creates an OpenAIError for missing client.

        Returns:
            OpenAIError: An instance of OpenAIError.
        """
        return cls("Client is required.")

    @classmethod
    def api_key_not_found(cls):
        """
        Creates an OpenAIError for a missing API key.

        Returns:
            OpenAIError: An instance of OpenAIError.
        """
        return cls("API key not found. Ensure the OPENAI_API_KEY environment variable is set.")


class WaybackMachineError(HTTPError, ConnectionError, Timeout, NewConnectionError):
    """
    Raised when an HTTP error occurs with the Wayback Machine.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message="Connection Failed"):
        super().__init__(f"Wayback Machine: {message}")
