import datetime
import logging
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from typing import List, Tuple, Optional

# Precompiled regex pattern for extracting names
NAME_PATTERN = re.compile(
    r'\b([A-Z][a-zA-Z]*\.?\s(?:[A-Z]\.\s)?[A-Z][a-zA-Z]+(?:-[A-Z][a-z]+)?'
    r'(?:\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?)?)\b'
)

# Set of generic email prefixes to be filtered out
GENERIC_EMAIL_PREFIXES = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply', 'philosophy'}


def extract_timestamps(url: str) -> pd.DataFrame:
    """
    Fetches a webpage from the given URL and extracts timestamps and metadata.

    Args:
        url (str): The URL of the webpage to be processed.

    Returns:
        pd.DataFrame: A DataFrame containing extracted student information.

    Raises:
        requests.ConnectionError: If a network problem occurs.
        requests.Timeout: If the request times out.
        requests.HTTPError: For HTTP-related errors.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.ConnectionError, requests.Timeout) as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    soup = BeautifulSoup(response.text, 'html.parser')
    [s.extract() for s in soup(['script', 'style'])]

    date, university, department, status = extract_metadata(url)
    names = extract_names(soup)

    student_timestamps = [
        {'Name': name, 'University': university, 'Department': department, 'URL': url, 'Date': date, 'Active': status}
        for name in names
    ]

    return pd.DataFrame(student_timestamps)


def extract_metadata(url: str) -> Tuple[datetime.datetime, str, str, bool]:
    """
    Extracts metadata from the URL.

    Args:
        url (str): The URL from which metadata is to be extracted.

    Returns:
        Tuple[datetime.datetime, str, str, bool]: A tuple containing the extracted date,
                                                  university name, department name, and
                                                  active status.

    Raises:
        IndexError: If the URL structure is not as expected and the date cannot be parsed.
    """
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0])
        status = False
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today())
        status = True

    path_elements = url.split('.edu')[0].split("/")[-1].split(".")
    university = path_elements[1]
    department = path_elements[0]

    return date, university, department, status


def extract_names(soup: BeautifulSoup) -> List[str]:
    """
    Extracts names based on email addresses found in the soup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the webpage content.

    Returns:
        List[str]: A list of names extracted from the webpage.
    """
    names = []
    mailto_elements = find_emails(soup)
    full_text = soup.get_text()  # Get the full text once to improve efficiency

    for el in mailto_elements:
        email = el.get_text().strip()
        email_prefix = email.split('@')[0]
        potential_names = match_name_pattern(full_text)
        best_match = max(potential_names,
                         key=lambda name: SequenceMatcher(None, email_prefix.lower(),
                                                          name.replace(' ', '').lower()).ratio(),
                         default=None)
        names.append(best_match)

    return names


def find_emails(soup: BeautifulSoup) -> List[BeautifulSoup]:
    """
    Finds email addresses in the soup object and filters out generic addresses.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to search within.

    Returns:
        List[BeautifulSoup]: A list of BeautifulSoup elements containing email addresses.
    """
    filtered_elements = []

    for el in soup.find_all(href=lambda x: x and 'mailto:' in x):
        email = el.get_text().strip()
        email_prefix = email.split('@')[0].lower()
        if not any(term in email_prefix for term in GENERIC_EMAIL_PREFIXES):
            filtered_elements.append(el)

    return filtered_elements


def match_name_pattern(text: str) -> List[str]:
    """
    Matches potential names in the given text based on a regex pattern.

    Args:
        text (str): The text in which to search for names.

    Returns:
        List[str]: A list of potential names found in the text.
    """
    return re.findall(NAME_PATTERN, text)
