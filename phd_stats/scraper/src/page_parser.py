import datetime
import logging
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from typing import Tuple
from ..src.names_extractor import extract_names


def extract_timestamps(url: str) -> pd.DataFrame:
    """
    Extracts student timestamps from the webpage snapshot URL.

    Args:
        url (str): The URL of the webpage snapshot.

    Returns:
        pd.DataFrame: A DataFrame containing extracted student timestamps.

    Raises:
        requests.ConnectionError: If a network problem occurs.
        requests.Timeout: If the request times out.
        requests.HTTPError: For HTTP-related errors.
    """
    columns = ['Name', 'University', 'Department', 'URL', 'Date', 'Active']
    data = []

    page_content = fetch_page_content(url)
    names, university, department = extract_names(page_content, url)
    date, status = parse_date(url)

    for name in names:
        data.append({
            'Name': name,
            'University': university,
            'Department': department,
            'URL': url,
            'Date': date,
            'Active': status
        })

    return pd.DataFrame(data, columns=columns)


def fetch_page_content(url, max_retries=5, retry_delay=60):
    """
    Fetches and parses the content of the given URL.

    Args:
        url (str): The URL to fetch.
        max_retries (int): Maximum number of retries for the request.
        retry_delay (int): Delay in seconds before retrying the request.

    Returns:
        BeautifulSoup: Parsed HTML content of the page, or None if the request fails.
    """
    attempts = 0

    while attempts < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()

            page_content = BeautifulSoup(response.text, 'html.parser')
            [s.extract() for s in page_content(['script', 'style'])]
            return page_content

        except (requests.ConnectionError, requests.Timeout) as e:
            logging.error(f"Retrying in {retry_delay}s - Network error fetching content of {url[:60]}...")
            attempts += 1
            time.sleep(retry_delay)

        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred while fetching {url}: {e}")
            break

    logging.error(f"Failed to fetch content from {url} after {max_retries} attempts.")
    return BeautifulSoup("", 'html.parser')


def parse_date(url: str) -> Tuple[datetime.datetime, bool]:
    """
    Extracts metadata from the webpage snapshot URL.

    Args:
        url (str): The URL of the webpage snapshot.

    Returns:
        Tuple[datetime.datetime, bool]: A tuple containing the date and active status.

    Raises:
        IndexError: If the URL structure is not as expected and the data cannot be parsed.
    """
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0]).strftime('%Y-%m-%d')
        status = False
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today()).strftime('%Y-%m-%d')
        status = True

    return date, status
