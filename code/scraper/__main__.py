import argparse
import logging
import csv
import pandas as pd

from .src.data_processor import process_data
from .src.page_parser import extract_timestamps
from .src.snapshot_fetcher import get_snapshots
from .src.update_placement import update_placement_from_webpage
from .src.utils import generate_report, update_dataset


def scrape_data(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        url_pairs = []
        for row in reader:
            url_pairs.append((row[0].split(' ')[0], row[0].split(' ')[1]))

    all_data = pd.DataFrame()

    for url, placement_url in url_pairs:

        snapshots = get_snapshots(url, log=True)

        list_data = pd.DataFrame()

        for snapshot in snapshots:
            snapshot_data = extract_timestamps(snapshot)
            list_data = pd.concat([list_data, snapshot_data], ignore_index=True)

        appearance_data = process_data(list_data)

        logging.info(f"Found {len(appearance_data)} new candidates.")

        updated_placement = update_placement_from_webpage(appearance_data, placement_url)

        all_data = pd.concat([updated_placement, all_data], ignore_index=True)

    all_data['Start_Date'] = pd.to_datetime(all_data['Start_Date'])
    all_data['End_Date'] = pd.to_datetime(all_data['End_Date'])

    return all_data


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Web scraper for student data.")
    parser.add_argument("file", type=str, help="The file with URLs.")
    parser.add_argument("--update", action='store_true', help="Enable update logic.")

    args = parser.parse_args()

    # pd.set_option('display.width', 1000)
    # pd.set_option('display.max_columns', None)

    new_data = scrape_data(args.file)

    if args.update:
        update_dataset(new_data)
    else:
        # new_data['Start_Date'] = pd.to_datetime(new_data['Start_Date'])
        # new_data['End_Date'] = pd.to_datetime(new_data['End_Date'])
        # pd.set_option('display.max_colwidth', None)
        # pd.set_option('display.max_rows', 100)
        # print(new_data)
        generate_report(new_data)
