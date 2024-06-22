"""
This module provides functions to fetch and process data from Wayback Machine snapshots of web pages.
It includes functionality to handle pagination, retry failed requests, and extract and process student timestamps.

Functions:
    add_data_from_pages(data, program_tuple, page_urls) -> pd.DataFrame:
        Adds data from paginated web pages to the existing DataFrame.

    get_pagination(url_tuple) -> List[str]:
        Generates a list of paginated URLs for the given base URL.

    get_page(url, max_retries=10, initial_retry_delay=16) -> str:
        Fetches and returns the content of the given URL with retry logic that doubles the delay after each failed attempt.

    _track_presence_in_page(page_tuple, log_snapshot_search) -> pd.DataFrame:
        Tracks and processes student presence data from a given URL page.

    _extract_timestamps_from_snapshot(page_source, url, university=None) -> pd.DataFrame:
        Extracts student timestamps from the webpage snapshot.

    _parse_date(url) -> Tuple[str, bool]:
        Parses the date and status from the snapshot URL.
"""

import logging
from typing import Tuple, List

import requests
import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError, Timeout

from ..src.search_module import search_names
from ..src.snapshot_url import get_snapshot_urls
from ..src.module_manager import generate_search_module, validate_search_module
from ..src.database import process_data
from ..src.exceptions import ValidationError, ModuleError


def scrape_data_from_pages(
        data: pd.DataFrame,
        program_tuple: Tuple[str, str, str],
        page_urls: List[str]
) -> pd.DataFrame:
    """
        Adds data from paginated web pages to the existing DataFrame.

        Args:
            data (pd.DataFrame): The existing DataFrame to append new data to.
            program_tuple (Tuple[str, str, str]): A tuple containing the base URL, placement URL, and program name.
            page_urls (List[str]): A list of paginated URLs to fetch data from.

        Returns:
            pd.DataFrame: Updated DataFrame with new data appended.
        """
    log = True
    for url_page in page_urls:
        page_tuple = (url_page, program_tuple[1], program_tuple[2])
        data_from_url = _track_presence_in_page(page_tuple, log)
        log = False
        data = pd.concat([data_from_url, data], ignore_index=True)

    if not data.empty:
        data['Start_Date'] = pd.to_datetime(data['Start_Date'])
        data['End_Date'] = pd.to_datetime(data['End_Date'])

    return data


def load_search_module(validation_url):
    """
    Validate or generate the search function.

    Args:
        validation_url: The URL to validate the function.
    Returns:
        None
    """
    validation_html = get_page(validation_url)
    try:
        validate_search_module(validation_html, validation_url)
    except (ValidationError, ModuleError):
        generate_search_module(validation_html, validation_url)
    # save snapshot items to a text file
    # with open('scraper/tests/snapshots.csv', 'w') as file:
    #     for url in snapshot_urls:
    #         file.write(url + '\n')

    # with open('scraper/tests/validation_2024-06-09.html', 'r') as file:
    #     validation_html = file.read()
    #
    # with open('scraper/tests/snapshots.csv', 'r') as file:
    #     snapshot_urls = file.read().splitlines()

    # with open(f'scraper/tests/validation_{parse_date(url)[0]}.html', 'r') as file:
    #     page_source = file.read()


def get_pagination(url_tuple: tuple) -> list:
    """
    Generates a list of paginated URLs for the given base URL.

    Args:
        url_tuple (tuple): A tuple containing the base URL, placement URL, and program name.

    Returns:
        list: A list of paginated URLs.
    """
    url = url_tuple[0]
    url_pages = [url]
    previous_response = get_page(url)

    i = 2
    while i < 1000:
        url_page = url + f'?pg={i}'
        response = get_page(url_page)

        soup = BeautifulSoup(response, 'html.parser')

        try:
            empty_h1_tags = soup.find('h1', {'class': 'plain'}).text.strip() == ""
        except:
            empty_h1_tags = None

        if empty_h1_tags or abs(len(response) - len(previous_response)) <= 50:
            logging.info(f"Found {i - 1} page{'s' if len(url_pages) > 1 else ''} for {url_tuple[2]}")
            break

        url_pages.append(url_page)
        previous_response = response
        i += 1

    return url_pages

# todo: factor out page identity (or empty) check function


def get_page(url: str, max_retries: int = 10, initial_retry_delay: int = 16) -> str:
    """
    Fetches and returns the content of the given URL with retry logic that doubles the delay after each failed attempt.

    Args:
        url (str): The URL to fetch.
        max_retries (int): Maximum number of retries for the request. Default is 10.
        initial_retry_delay (int): Initial delay in seconds before retrying the request. Default is 16.

    Returns:
        str: The content of the page as text, or an empty string if the request fails.
    """
    attempts = 0
    retry_delay = initial_retry_delay

    while attempts < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text

        except (HTTPError, ConnectionError, Timeout):
            logging.error(f"Retrying in {retry_delay}s - Wayback Machine connection failed")
            time.sleep(retry_delay)
            retry_delay *= 2
            attempts += 1

    logging.error(f"Failed to fetch content after {max_retries} attempts.")
    return ""
    # page_content = BeautifulSoup(response.text, 'html.parser')
    # [s.extract() for s in page_content(['script', 'style'])]
    # return page_content
    # return BeautifulSoup("", 'html.parser')


def _track_presence_in_page(page_tuple: Tuple[str, str, str], log_snapshot_search: bool) -> pd.DataFrame:
    """
    Tracks and processes student presence data from a given URL page.

    Args:
        page_tuple (Tuple[str, str, str]): A tuple containing the URL, placement URL, and program name.
        log_snapshot_search (bool): Whether to log the snapshot search.

    Returns:
        pd.DataFrame: DataFrame with processed and updated data.
    """
    snapshot_urls = get_snapshot_urls(page_tuple, log=log_snapshot_search)

    list_data = pd.DataFrame()

    for url in snapshot_urls:
        page_source = get_page(url)
        load_search_module(validation_url=url)
        snapshot_data = _extract_timestamps_from_snapshot(page_source, url, university=page_tuple[2])
        list_data = pd.concat([list_data, snapshot_data], ignore_index=True)

    presence_data = process_data(list_data, log=True)

    return presence_data


def _extract_timestamps_from_snapshot(page_source: str, url: str, university: str = None) -> pd.DataFrame:
    """
    Extracts student timestamps from the webpage snapshot.

    This function parses the provided HTML content of a webpage snapshot to extract student names
    and associated metadata such as the university, URL, date, and active status. It returns the
    extracted information as a pandas DataFrame with the following columns:
            - Name: The name of the student.
            - University: The name of the university.
            - URL: The URL of the webpage snapshot.
            - Date: The date of the snapshot.
            - Active: The active status of the student.

    Args:
        page_source (str): The HTML source code of the page.
        url (str): The URL of the webpage snapshot.
        university (str, optional): The name of the university. Default is None.

    Returns:
        pd.DataFrame: A DataFrame containing extracted student timestamps.

    Raises:
        SystemExit: If an unexpected error occurs during the name search process.
    """
    columns = ['Name', 'University', 'URL', 'Date', 'Active']
    data = []

    try:
        names = search_names(page_source, url)
    except Exception as e:
        logging.error(e)
        names = []
        # logging.fatal(
        #     "An unexpected error occurred during the name search process. "
        #     "Please check the log for more details and try running the program again.",
        #     exc_info=True
        # )
    print("Extracted names: ", names)
    date, status = _parse_date(url)

    for name in names:
        data.append({
            'Name': name,
            'University': university,
            'URL': url,
            'Date': date,
            'Active': status
        })

    return pd.DataFrame(data, columns=columns)
    # save page source to html in scraper/tests/validation_number.html where number is next available index
    # with open(f'scraper/tests/validation_{date}.html', 'w') as file:
    #     file.write(page_source)


def _parse_date(url: str) -> Tuple[str, bool]:
    """
    Parses the date and status from the snapshot URL.

    Args:
        url (str): The URL of the webpage snapshot.

    Returns:
        Tuple[str, bool]: A tuple containing the date and active status.
    """
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0]).strftime('%Y-%m-%d')
        status = False
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today()).strftime('%Y-%m-%d')
        status = True

    return date, status
