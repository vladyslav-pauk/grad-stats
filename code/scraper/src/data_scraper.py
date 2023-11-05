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
            snapshots = snapshot_fetcher.get_snapshots(log=True)

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', None)

    new_data = scrape_data(['https://philosophy.arizona.edu/phd-students'])
    logging.info(f"Data has been processed. {len(new_data)} new data samples found.")

    new_data['Start_Date'] = pd.to_datetime(new_data['Start_Date'])
    new_data['End_Date'] = pd.to_datetime(new_data['End_Date'])
    print(new_data['Snapshots'].apply(lambda x: len(x)))
