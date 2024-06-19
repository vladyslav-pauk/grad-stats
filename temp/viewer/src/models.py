import os
import pickle
import sys
from datetime import datetime

sys.path.append('/phd-stats/')


def get_latest_version(data_folder='dataset') -> int:
    """
    Gets the latest version number of student data files in the specified folder.

    Args:
        data_folder (str): The folder where the data files are located.

    Returns:
        int: The latest version number or None if no valid files are found.

    Raises:
        OSError: If the specified data folder does not exist.
    """
    versions = []
    full_path = os.path.join(os.getcwd(), data_folder)
    if not os.path.exists(full_path):
        raise OSError(f"DataTable folder {data_folder} not found.")

    for filename in os.listdir(full_path):
        if filename.startswith("student_data_v"):
            try:
                version_number = int(filename.split('_v')[1].split('.pkl')[0])
                versions.append(version_number)
            except ValueError:
                continue  # Skip files with invalid version formatting
    return max(versions, default=None)


def get_latest_data_path(base_path: str) -> str:
    """
    Constructs the file path for the latest version of the student data.

    Args:
        base_path (str): Base path to the data files.

    Returns:
        str: File path to the latest data file.

    Raises:
        ValueError: If no latest version is found.
    """
    latest_version = get_latest_version(base_path)
    if latest_version is None:
        raise ValueError("No latest version found.")
    return os.path.join(os.getcwd(), base_path, f'student_data_v{latest_version}.pkl')


def load_dataframe(data_path: str):
    """
    Loads a DataFrame from a pickled file.

    Args:
        data_path (str): Path to the pickled file.

    Returns:
        DataFrame or None: Loaded DataFrame or None if loading fails.

    Raises:
        FileNotFoundError: If the specified data file does not exist.
        pickle.UnpicklingError, EOFError: If an error occurs during the unpickling process.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"DataTable file {data_path} not found.")

    try:
        with open(data_path, "rb") as file:
            return pickle.load(file)
    except (pickle.UnpicklingError, EOFError) as e:
        raise e


def get_snapshot_dates(df, url: str) -> list:
    """
    Extracts snapshot dates for a given URL from a DataFrame.

    Args:
        df (DataFrame): The DataFrame containing snapshot data.
        url (str): URL to filter snapshots.

    Returns:
        list: A list of dictionaries with snapshot URLs and their respective dates.

    Raises:
        KeyError: If the DataFrame does not contain 'URL' or 'Snapshots' columns.
    """
    if 'URL' not in df.columns or 'Snapshots' not in df.columns:
        raise KeyError("DataFrame must contain 'URL' and 'Snapshots' columns.")

    snapshots = df[df['URL'] == url]['Snapshots'].explode().unique()
    return [{'url': snap, 'date': extract_date_from_url(snap)} for snap in sorted(snapshots, reverse=True)]


def extract_date_from_url(url: str) -> str:
    """
    Extracts and formats the date from a URL string.

    Args:
        url (str): The URL string containing the date.

    Returns:
        str: The extracted and formatted date.

    Raises:
        ValueError: If the date cannot be extracted from the URL.
    """
    try:
        if '/web/' in url:
            date_str = url.split('/web/')[1].split('/')[0][:-6]  # Remove HMS
            return datetime.strptime(date_str, "%Y%m%d").strftime("%m/%d/%Y")
    except Exception:
        raise ValueError(f"Unable to extract date from URL: {url}")

    return datetime.now().strftime("%m/%d/%Y")
