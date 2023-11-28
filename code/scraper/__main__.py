import argparse
import logging

import pandas as pd
from ydata_profiling import ProfileReport

from .src.data_processor import process_data
from .src.page_parser import extract_timestamps
from .src.snapshot_fetcher import get_snapshots
from .src.utils import get_latest_version, merge_and_save


def scrape_data(urls):
    all_data = pd.DataFrame()

    for url in urls:

        logging.info('Scraping ' + url + '...')
        snapshots = get_snapshots(url, log=True)

        list_data = pd.DataFrame()

        for snapshot in snapshots:
            snapshot_data = extract_timestamps(snapshot)
            list_data = pd.concat([list_data, snapshot_data], ignore_index=True)

        appearance_data = process_data(list_data)
        all_data = pd.concat([appearance_data, all_data], ignore_index=True)

    return all_data


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Web scraper for student data.")
    parser.add_argument("url", type=str, help="The URL to scrape data from.")
    parser.add_argument("--update", action='store_true', help="Enable update logic.")

    args = parser.parse_args()

    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', None)

    new_data = scrape_data([args.url])
    logging.info(f"Data has been processed. {len(new_data)} new data samples found.")

    if args.update:
        latest_version = get_latest_version()
        if latest_version is None:
            logging.info("No previous versions found. Creating new data file.")
            latest_version = 0
        else:
            logging.info(f"Current version of data is v{latest_version}")

        new_version = merge_and_save(new_data, latest_version)

        if new_version is not None:
            logging.info(f"Data updated. New version is v{new_version}.")
    else:
        new_data['Start_Date'] = pd.to_datetime(new_data['Start_Date'])
        new_data['End_Date'] = pd.to_datetime(new_data['End_Date'])
        # pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 100)
        print(new_data)
        profile = ProfileReport(new_data, title="Profiling Report")
        report_path = "dataset/student_report.html"
        profile.to_file(report_path)
        logging.info(f"Profiling report generated at {report_path}")
