import argparse
import logging

import pandas as pd
from ydata_profiling import ProfileReport

from .src.data_scraper import scrape_data
from .src.utils import get_latest_version, merge_and_save

# todo: make those inline comments
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
        print(new_data)
        profile = ProfileReport(new_data, title="Profiling Report")
        report_path = "reports/student_report.html"
        profile.to_file(report_path)
        logging.info(f"Profiling report generated at {report_path}")
