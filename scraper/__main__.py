# This file is the entry point for the scraper package.
# The package is used to scrape data on graduation and placement records of PhD students in Philosophy.
# It reads URLs from a CSV file, consolidates scraped data from each URL, and updates the dataset.

import argparse
import csv
import pandas as pd
import logging

from .src.data_aggregator import process_data
from .src.page_parser import extract_timestamps, fetch_page, parse_date
from .src.snapshot_fetcher import get_snapshots
from .src.placement_updater import update_placement_from_webpage
from .src.utils import update_dataset
from .src.code_generator import generate_function, validate_function
from .src.utils import init_gpt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
client, _ = init_gpt()


def scrape_data(filename: str) -> pd.DataFrame:
    """
    Reads URLs from a CSV file and consolidates scraped data from each URL.

    Args:
        filename (str): Path to the CSV file containing URLs.

    Returns:
        pd.DataFrame: Aggregated DataFrame containing data from all URLs.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        csv.Error: If there is an error in reading the CSV file.
        ValueError: If URL processing fails.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        url_pairs = []
        for row in reader:
            url_pairs.append((row[0].split(' ')[0], row[0].split(' ')[1]))

    all_data = pd.DataFrame()

    # url_pairs = [('http://philosophy.princeton.edu:80/people/graduate-students', 'https://philosophy.princeton.edu/graduate/placement-record')]

    for url, placement_url in url_pairs:
        data_from_url = get_data_from_url(url, placement_url)
        all_data = pd.concat([data_from_url, all_data], ignore_index=True)

    if not all_data.empty:
        all_data['Start_Date'] = pd.to_datetime(all_data['Start_Date'])
        all_data['End_Date'] = pd.to_datetime(all_data['End_Date'])

    return all_data


def get_data_from_url(url: str, placement_url: str) -> pd.DataFrame:
    """
    Scrapes data from a given URL, processes it, and updates placement information.

    Args:
        url (str): The URL to scrape data from.
        placement_url (str): The URL to update placement information.

    Returns:
        pd.DataFrame: DataFrame with processed and updated data.

    Raises:
        requests.exceptions.RequestException: If an error occurs during URL fetching.
        ValueError, RuntimeError: If data processing or placement updating fails.
    """

    # save snapshot items to a text file
    # with open('scraper/tests/snapshots.csv', 'w') as file:
    #     for url in snapshot_urls:
    #         file.write(url + '\n')

    # with open('scraper/tests/validation_2024-06-09.html', 'r') as file:
    #     validation_html = file.read()
    #
    # with open('scraper/tests/snapshots.csv', 'r') as file:
    #     snapshot_urls = file.read().splitlines()

    snapshot_urls = get_snapshots(url, log=True)
    validation_html = fetch_page(snapshot_urls[0])

    if not validate_function(validation_html, url):
        generate_function(validation_html, url, client)

    list_data = pd.DataFrame()

    for url in snapshot_urls:
        page_source = fetch_page(url)
        # with open(f'scraper/tests/validation_{parse_date(url)[0]}.html', 'r') as file:
        #     page_source = file.read()

        snapshot_data = extract_timestamps(page_source, url)
        list_data = pd.concat([list_data, snapshot_data], ignore_index=True)

    appearance_data = process_data(list_data)

    data_with_updated_placement = update_placement_from_webpage(appearance_data, placement_url)
    return data_with_updated_placement


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Web scraper for student data.")
    parser.add_argument("file", nargs='?', default="scraper/urls.csv", type=str, help="The file with URLs.")

    args = parser.parse_args()

    if args.file is None:
        new_data = scrape_data('urls.csv')
    else:
        new_data = scrape_data(args.file)

    update_dataset(new_data)
