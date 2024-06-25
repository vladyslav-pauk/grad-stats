import logging
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def update_placement(database_df: pd.DataFrame, placement_page: str, log: bool = True) -> pd.DataFrame:
    """
    Update 'Placement' column in the database dataframe with names found in the placement webpage.

    This function sends a request to the specified URL and updates the 'Placement' column in the provided
    DataFrame to True for names that are found on the webpage. If the 'Placement' column does not exist,
    it is created.

    Args:
        placement_page:
        log:
        database_df (pd.DataFrame): DataFrame containing the database with a 'Name' column.

    Returns:
        pd.DataFrame: Updated DataFrame with 'Placement' column reflecting found names.
                     If an HTTP error occurs, the original DataFrame is returned without changes.

    Raises:
        requests.RequestException: If there is an error in fetching the webpage.
                                   The error is logged, and the function returns the original DataFrame.
    """
    if 'Placement' not in database_df.columns:
        database_df['Placement'] = False

    # Add the placement_page URL to a new column in the DataFrame
    database_df['PlacementURL'] = placement_page

    try:
        response = requests.get(placement_page)
        response.raise_for_status()
        response_content = response.content
        soup_object = BeautifulSoup(response_content, 'html.parser')
        html_content = soup_object.get_text()
    except requests.RequestException:
        logging.error(f"Error fetching placement page {placement_page}")
        html_content = ''

    webpage_names = set(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', html_content))

    def preprocess_name(name):
        return sorted(name.replace(',', '').split())

    def check_two_word_match(name_parts, webpage_name_parts_list):
        for webpage_name_parts in webpage_name_parts_list:
            match_count = sum(part in webpage_name_parts for part in name_parts)
            if match_count >= 2:
                return True
        return False

    database_df['ProcessedName'] = database_df['Name'].apply(preprocess_name)

    processed_webpage_names = [preprocess_name(name) for name in webpage_names]

    database_df['Placement'] = database_df['ProcessedName'].apply(
        lambda x: check_two_word_match(x, processed_webpage_names))

    database_df.drop('ProcessedName', axis=1, inplace=True)

    matching_placements = database_df['Placement'].sum()

    if log:
        logging.info(f"Found {matching_placements} placements")

    return database_df
