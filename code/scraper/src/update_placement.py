# File: name_matcher.py
import pickle
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def update_placement_from_webpage(database_df, url):
    """
    Update 'Placement' column in the database dataframe with names found in the webpage.

    :param database_df: DataFrame containing the database with a 'Name' column
    :param url: URL of the webpage to search for names
    :return: Updated DataFrame with 'Placement' column reflecting found names
    """
    # Step 1: Check if 'Placement' column exists, if not add it
    if 'Placement' not in database_df.columns:
        database_df['Placement'] = False  # Initialize with 0 (not placed)

    # Step 2: Fetch and parse the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Step 3: Find all names in the webpage
    webpage_names = set(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text))

    # Step 4: Match and update Placement
    webpage_names_set = set(webpage_names)

    # Create a new column 'Placement' with True if the 'Name' is in 'webpage_names_set', otherwise False
    database_df['Placement'] = database_df['Name'].isin(webpage_names_set)

    return database_df


# Usage example
# Assuming you have a pandas DataFrame named `db_df` and a URL to match names against
path_to_dataset = '/Users/studio/Work/Projects/Education/code/'
latest_data_path = f'{path_to_dataset}dataset/student_data_v2.pkl'
with open(latest_data_path, "rb") as f:
    df = pickle.load(f)

updated_db_df = update_placement_from_webpage(df, 'https://philosophy.arizona.edu/phd-philosophy/placements')

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(updated_db_df)
