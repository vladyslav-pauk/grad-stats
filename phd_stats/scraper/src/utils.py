import logging
import os
import pickle

import pandas as pd


def update_dataset(new_data):
    """
        Updates the dataset with new data and increments the version.

        Args:
            new_data (pd.DataFrame): The new data to be merged with the existing dataset.

        Raises:
            IOError: If an I/O operation fails during data processing.
        """
    latest_version = get_latest_version()
    if latest_version is None:
        logging.info("No previous versions found. Creating new data file.")
        latest_version = 0
    else:
        logging.info(f"Current version of data is v{latest_version}")

    new_version = merge_and_save(new_data, latest_version)

    if new_version is not None:
        logging.info(f"Data updated. New version is v{new_version}.")


def get_latest_version(data_folder='dataset'):
    """
        Retrieves the latest version number of the dataset.

        Args:
            data_folder (str): The folder where the data files are stored.

        Returns:
            int: The latest version number or None if no versions are found.

        Raises:
            OSError: If there is an issue accessing the data folder.
        """
    versions = []

    data_folder = os.path.join(os.getcwd(), data_folder)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for filename in os.listdir(data_folder):
        if filename.startswith("student_data_v"):
            version_number = int(filename.split('_v')[1].split('.pkl')[0])
            versions.append(version_number)
    return max(versions, default=None)


def merge_and_save(new_data, latest_version, data_folder='dataset'):
    """
        Merges new data with existing data and saves it.

        Args:
            new_data (pd.DataFrame): The new data to merge.
            latest_version (int): The latest version number of the existing data.
            data_folder (str): The folder where the data files are stored.

        Returns:
            int: The new version number of the dataset.

        Raises:
            IOError: If an I/O operation fails during data merging or saving.
            ValueError: If there is an issue in data processing.
        """
    old_data_path = os.path.join(data_folder, f'student_data_v{latest_version}.pkl')

    if os.path.exists(old_data_path):
        try:
            with open(old_data_path, "rb") as f:
                old_data = pickle.load(f)
        except:
            old_data = pd.DataFrame()

        merged_data = pd.concat([old_data, new_data], ignore_index=True)
        total_entries = len(merged_data)
        duplicate_entries = merged_data.duplicated(subset=['Name']).sum()
        if len(new_data) == 0:
            logging.info("No new entries found. Skipping update.")
            return None

        if duplicate_entries == len(new_data):
            logging.info("All new entries are duplicates. Skipping update.")
            return None

        logging.info(f"Number of new items added: {total_entries - duplicate_entries}")

        merged_data = merged_data.drop_duplicates(subset=['Name'])
    else:
        merged_data = new_data

    new_version = latest_version + 1
    with open(os.path.join(data_folder, f'student_data_v{new_version}.pkl'), "wb") as f:
        pickle.dump(merged_data, f)

    return new_version


def view_data(latest_data_path):
    """
        Prints the data from the latest dataset.

        Args:
            latest_data_path (str): The path to the latest data file.

        Raises:
            IOError: If the data file cannot be opened or read.
            pickle.UnpicklingError: If there is an error unpickling the data.
        """
    with open(latest_data_path, "rb") as f:
        df = pickle.load(f)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        print(df['Snapshots'].apply(lambda x: len(x)))
