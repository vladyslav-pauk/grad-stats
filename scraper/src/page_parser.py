import datetime
import logging
import requests
import pandas as pd
import time
# from bs4 import BeautifulSoup
from typing import Tuple
from ..src.names_extractor import search_names
from ..src.utils import extract_filepath


def extract_timestamps(page_source: str, url: str) -> pd.DataFrame:
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

    filepath = extract_filepath(url)
    department, university = filepath.rsplit('/', 1)[-1].split('_')[:2]
    university = university.split('.')[0]

    names = search_names(page_source, filepath)

    date, status = parse_date(url)

    # save page source to html in scraper/tests/validation_number.html where number is next available index
    # with open(f'scraper/tests/validation_{date}.html', 'w') as file:
    #     file.write(page_source)

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


def fetch_page(url, max_retries=5, retry_delay=120):
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

            # page_content = BeautifulSoup(response.text, 'html.parser')
            # [s.extract() for s in page_content(['script', 'style'])]
            return response.text
            # return page_content

        except (requests.ConnectionError, requests.Timeout) as e:
            # logging.error(f"Retrying in {retry_delay}s - Network error fetching content of {url[:60]}...")
            logging.error(f"Retrying in {retry_delay}s - Network error occurred.")
            attempts += 1
            time.sleep(retry_delay)

        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred while fetching {url}: {e}")
            break

    logging.error(f"Failed to fetch content from {url} after {max_retries} attempts.")
    # return BeautifulSoup("", 'html.parser')
    return ""


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
