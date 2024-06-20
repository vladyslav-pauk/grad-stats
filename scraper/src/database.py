"""
This module provides functions to update, process, and view a dataset of student information.
It includes functionality to merge new data, process existing data, and calculate yearly metrics.

Functions:
    update_dataset(new_data: pd.DataFrame) -> None:
        Updates the dataset with new data and increments the version.

    process_data(data: pd.DataFrame, log: bool) -> pd.DataFrame:
        Processes student data to create a summary DataFrame.

    view_data(latest_data_path: str) -> None:
        Prints the data from the latest dataset.

    calculate_yearly_metrics(data: pd.DataFrame) -> pd.DataFrame:
        Calculates yearly metrics for students.

    _get_latest_version(data_folder: str = 'public/data') -> int:
        Retrieves the latest version number of the dataset.

    _merge_and_save(new_data: pd.DataFrame, latest_version: int, data_folder: str = 'public/data') -> int:
        Merges new data with existing data and saves it.
"""

import numpy as np
from typing import Dict
import pandas as pd
import logging
import json
import os

from .utils import parent_url


def update_dataset(new_data: pd.DataFrame) -> None:
    """
    Updates the dataset with new data and increments the version.

    Args:
        new_data (pd.DataFrame): The new data to be merged with the existing dataset.

    Raises:
        IOError: If an I/O operation fails during data processing.
    """
    latest_version = _get_latest_version()
    if latest_version is None:
        # logging.info("Creating new data file")
        latest_version = 0
    # else:
        # logging.info(f"Current version of data is v{latest_version}")

    new_version = _merge_and_save(new_data, latest_version)

    if new_version is not None:
        logging.info(f"Dataset updated to version v{new_version}")


def process_data(data: pd.DataFrame, log: bool) -> pd.DataFrame:
    """
    Processes student data to create a summary DataFrame.

    Args:
        data (pd.DataFrame): The original dataset containing student information.
        log (bool): Whether to log the processing information.

    Returns:
        pd.DataFrame: A processed DataFrame with summarized information for each student.

    Raises:
        ValueError: If there is an issue with data format or content.
        KeyError: If expected columns are not present in the DataFrame.
    """
    columns = ['Name', 'University', 'URL', 'Date', 'Active', 'Placement', 'Years', 'Snapshots']
    student_info = pd.DataFrame(columns=columns)

    try:
        data['Date'] = pd.to_datetime(data['Date'])

        student_info = data.groupby('Name').agg(
            University=('University', 'first'),
            URL=('URL', lambda x: parent_url(x.iloc[0])),
            Start_Date=('Date', 'min'),
            End_Date=('Date', 'max'),
            Active=('Active', 'sum')
        )

        student_info['Years'] = (student_info['End_Date'] - student_info['Start_Date']).dt.days / 365.25
        student_info['Active'] = student_info['Active'] > 0

        student_info['Snapshots'] = data.groupby('Name')['URL'].unique()

        if log:
            logging.info(f"Found {len(student_info)} candidates in {len(data)} timestamps")
    except Exception as e:
        logging.error(f"Error processing data: {e}")

    return student_info.reset_index()


def view_data(latest_data_path: str) -> None:
    """
    Prints the data from the latest dataset.

    Args:
        latest_data_path (str): The path to the latest data file.
    """
    with open(latest_data_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        print(df['Snapshots'].apply(lambda x: len(x)))


def calculate_yearly_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates yearly metrics for students.

    Args:
        data (pd.DataFrame): The DataFrame containing student data with date information.

    Returns:
        pd.DataFrame: A DataFrame summarizing the total and graduated students per year.
    """
    data['Year'] = data['Date'].dt.year

    agg_dict: Dict[str, pd.NamedAgg] = {
        'Total_Students': pd.NamedAgg(column='Name', aggfunc='nunique'),  # Count of unique students per year
        'Graduated_Students': pd.NamedAgg(
            column='End_Date',
            aggfunc=lambda x: (x < data['Date'].max()).sum()  # Count of students graduated till the last date in data
        )
    }
    return data.groupby('Year').agg(**agg_dict)


def _get_latest_version(data_folder: str = 'public/data') -> int:
    """
    Retrieves the latest version number of the dataset.

    Args:
        data_folder (str): The folder where the data files are stored.

    Returns:
        int: The latest version number or None if no versions are found.
    """
    versions = []

    data_folder = os.path.join(os.getcwd(), data_folder)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for filename in os.listdir(data_folder):
        if filename.startswith("student_data_v"):
            version_number = int(filename.split('_v')[1].split('.json')[0])
            versions.append(version_number)
    return max(versions, default=None)


def _merge_and_save(new_data: pd.DataFrame, latest_version: int, data_folder: str = 'public/data') -> int:
    """
    Merges new data with existing data and saves it.

    Args:
        new_data (pd.DataFrame): The new data to merge.
        latest_version (int): The latest version number of the existing data.
        data_folder (str): The folder where the data files are stored.

    Returns:
        int: The new version number of the dataset.
    """
    old_data_path = os.path.join(data_folder, f'student_data_v{latest_version}.json')

    if os.path.exists(old_data_path):
        try:
            with open(old_data_path, 'r') as file:
                old_data = pd.DataFrame(json.load(file))
        except:
            old_data = pd.DataFrame()

        merged_data = pd.concat([old_data, new_data], ignore_index=True)
        total_entries = len(merged_data)
        duplicate_entries = merged_data.duplicated(subset=['Name']).sum()
        if len(new_data) == 0:
            logging.info("No new entries found. Skipping update.")
            return None

        if duplicate_entries == len(new_data):
            logging.info("Entries already exist - Skipping update")
            return None

        logging.info(f"Items added {total_entries - duplicate_entries}")

        merged_data = merged_data.drop_duplicates(subset=['Name'])
    else:
        merged_data = new_data

    for column in merged_data.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        merged_data[column] = merged_data[column].dt.strftime('%Y-%m-%d %H:%M:%S')

    for column in merged_data.columns:
        if merged_data[column].dtype == 'object':
            merged_data[column] = merged_data[column].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

    def convert_to_serializable(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    data_to_save = json.loads(json.dumps(merged_data.to_dict(orient='records'), default=convert_to_serializable))

    new_version = latest_version + 1
    with open(os.path.join(data_folder, f'student_data_v{new_version}.json'), 'w') as file:
        json.dump(data_to_save, file, indent=4)

    # with open(os.path.join(data_folder, f'versions.json'), 'wb') as file:
    #     pickle.dump({"latest_version": 2}, file)

    with open(os.path.join(data_folder, f'versions.json'), 'w') as file:
        json.dump({"latest_version": new_version}, file, indent=4)

    return new_version
