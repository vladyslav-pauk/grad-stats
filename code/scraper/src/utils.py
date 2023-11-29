import logging
import os
import pickle

import pandas as pd
from ydata_profiling import ProfileReport


def update_dataset(new_data):
    latest_version = get_latest_version()
    if latest_version is None:
        logging.info("No previous versions found. Creating new data file.")
        latest_version = 0
    else:
        logging.info(f"Current version of data is v{latest_version}")

    new_version = merge_and_save(new_data, latest_version)

    if new_version is not None:
        logging.info(f"Data updated. New version is v{new_version}.")


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

        merged_data = pd.concat([old_data, new_data], ignore_index=True)
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


def generate_report(new_data, version=''):

    profile = ProfileReport(new_data, title="Profiling Report", progress_bar=False, minimal=True)
    report_path = f"dataset/data_profile_{version}.html"
    profile.to_file(report_path)
    logging.info(f"Profiling report generated and saved to {report_path}")