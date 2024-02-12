import logging
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def update_placement_from_webpage(database_df: pd.DataFrame, url: str) -> pd.DataFrame:
    """
    Update 'Placement' column in the database dataframe with names found in the placement webpage.

    This function sends a request to the specified URL and updates the 'Placement' column in the provided
    DataFrame to True for names that are found on the webpage. If the 'Placement' column does not exist,
    it is created.

    Args:
        database_df (pd.DataFrame): DataFrame containing the database with a 'Name' column.
        url (str): URL of the webpage to search for names.

    Returns:
        pd.DataFrame: Updated DataFrame with 'Placement' column reflecting found names.
                     If an HTTP error occurs, the original DataFrame is returned without changes.

    Raises:
        requests.RequestException: If there is an error in fetching the webpage.
                                   The error is logged, and the function returns the original DataFrame.
    """
    if 'Placement' not in database_df.columns:
        database_df['Placement'] = False

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return database_df

    soup_object = BeautifulSoup(response.content, 'html.parser')
    html_content = soup_object.get_text()

    webpage_names = set(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', html_content))

    def preprocess_name(name):
        # Split the name into parts and sort them alphabetically
        return sorted(name.replace(',', '').split())

    def check_two_word_match(name_parts, webpage_name_parts_list):
        # Check if at least two words match between the name parts and any of the webpage name parts
        for webpage_name_parts in webpage_name_parts_list:
            match_count = sum(part in webpage_name_parts for part in name_parts)
            if match_count >= 2:
                return True
        return False

    # Preprocess all names in the database
    database_df['ProcessedName'] = database_df['Name'].apply(preprocess_name)

    # Preprocess all names from the webpage
    processed_webpage_names = [preprocess_name(name) for name in webpage_names]

    # Check if at least two words in the processed name from the database match with any of the processed webpage names
    database_df['Placement'] = database_df['ProcessedName'].apply(
        lambda x: check_two_word_match(x, processed_webpage_names))

    database_df.drop('ProcessedName', axis=1, inplace=True)

    matching_placements = database_df['Placement'].sum()
    logging.info(f"Found {matching_placements} placements in {url}")

    return database_df
