import logging

import pandas as pd

from .data_processor import DataProcessor
from .page_parser import PageParser
from .snapshot_fetcher import SnapshotFetcher


def scrape_data(urls):
    # path_to_dataset = '/Users/studio/Work/Projects/Education/code/'
    # latest_data_path = f'{path_to_dataset}dataset/student_data_v1.pkl'
    # with open(latest_data_path, "rb") as f:
    #     df = pickle.load(f)
    #     return df

    all_data = pd.DataFrame()

    for list_url in urls:
        try:
            logging.info('Scraping ' + list_url + '...')
            snapshot_fetcher = SnapshotFetcher(list_url)
            snapshots = snapshot_fetcher.get_snapshots()

            list_data = pd.DataFrame()

            for snapshot in snapshots:
                page_parser = PageParser(snapshot)
                snapshot_data = page_parser.extract_info()
                list_data = pd.concat([list_data, snapshot_data], ignore_index=True)

            data_transformer = DataProcessor(list_data)
            appearance_data = data_transformer.apply()

            all_data = pd.concat([appearance_data, all_data], ignore_index=True)
            # fixme: remove index from dataframe (or ydata))

        except Exception as e:
            logging.info(f"Failed to scrape {list_url}. Error: {e}")

    return all_data

# todo: add __main__ logic
