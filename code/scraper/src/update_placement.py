# File: update_placement.py
import logging
import re
import requests
from bs4 import BeautifulSoup


def update_placement_from_webpage(database_df, url):
    """
    Update 'Placement' column in the database dataframe with names found in the placement webpage.

    :param database_df: DataFrame containing the database with a 'Name' column
    :param url: URL of the webpage to search for names
    :return: Updated DataFrame with 'Placement' column reflecting found names
    """
    if 'Placement' not in database_df.columns:
        database_df['Placement'] = False

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    webpage_names = set(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text))

    webpage_names_set = set(webpage_names)

    database_df['Placement'] = database_df['Name'].isin(webpage_names_set)
    matching_placements = database_df['Placement'].sum()
    logging.info(f"Found {matching_placements} placements in {url}.")

    return database_df
