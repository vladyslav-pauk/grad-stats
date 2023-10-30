import logging
import os
import pickle

import pandas as pd


def get_latest_version(data_folder='/Users/studio/Work/Projects/Education/code/dataset/'):
    versions = []
    for filename in os.listdir(data_folder):
        if filename.startswith("student_data_v"):
            version_number = int(filename.split('_v')[1].split('.pkl')[0])
            versions.append(version_number)
    return max(versions, default=None)


def merge_and_save(new_data, latest_version, data_folder='/Users/studio/Work/Projects/Education/code/dataset'):
    old_data_path = os.path.join(data_folder, f'student_data_v{latest_version}.pkl')

    if os.path.exists(old_data_path):
        try:
            with open(old_data_path, "rb") as f:
                old_data = pickle.load(f)
        except:
            old_data = pd.DataFrame()

        merged_data = pd.concat([old_data, new_data])
        total_entries = len(merged_data)
        duplicate_entries = merged_data.duplicated(subset=['Email']).sum()
        if len(new_data) == 0:
            logging.info("No new entries found. Skipping update.")
            return None

        if duplicate_entries == len(new_data):
            logging.info("All new entries are duplicates. Skipping update.")
            return None

        logging.info(f"Number of new items added: {total_entries - duplicate_entries}")

        merged_data = merged_data.drop_duplicates(subset=['Email'])
    else:
        merged_data = new_data

    new_version = latest_version + 1
    with open(os.path.join(data_folder, f'student_data_v{new_version}.pkl'), "wb") as f:
        pickle.dump(merged_data, f)

    return new_version
