import re
from typing import Dict
import pandas as pd
import logging

# Compiled regex pattern for extracting the original URL from a web archive link
URL_PATTERN = re.compile(r'https?://web\.archive\.org/web/\d+/(https?://.+)')


def clean_url(url: str) -> str:
    """Clean the archived URL to its original form.

    Args:
        url (str): The URL to be cleaned, typically from the web archive.

    Returns:
        str: The original URL if extractable, otherwise the input URL.

    Raises:
        re.error: If there is an error in regex matching.
    """
    match = URL_PATTERN.search(url)
    return match.group(1) if match else url


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Process student data to create a summary DataFrame.

    Args:
        data (DataFrame): The original dataset containing student information.

    Returns:
        DataFrame: A processed DataFrame with summarized information for each student.

    Raises:
        ValueError: If there is an issue with data format or content.
        KeyError: If expected columns are not present in the DataFrame.
    """
    # Convert the 'Date' column from string to datetime for better manipulation
    data['Date'] = pd.to_datetime(data['Date'])

    # Aggregate student data by name and compute various statistics
    student_info = data.groupby('Name').agg(
        University=('University', 'first'),  # First university listed for each student
        Department=('Department', 'first'),  # First department listed for each student
        URL=('URL', lambda x: clean_url(x.iloc[0])),  # Cleaned URL of the first entry
        Start_Date=('Date', 'min'),  # Earliest date found for each student
        End_Date=('Date', 'max'),  # Latest date found for each student
        Active=('Active', 'sum')  # Sum of 'Active' entries to check if student was ever active
    )

    # Calculate the duration in years and determine active status
    student_info['Years'] = (student_info['End_Date'] - student_info['Start_Date']).dt.days / 365.25
    student_info['Active'] = student_info['Active'] > 0
    # List of unique URLs (snapshots) associated with each student
    student_info['Snapshots'] = data.groupby('Name')['URL'].unique()

    logging.info(f"Found {len(student_info)} new candidates.")

    return student_info.reset_index()


def calculate_yearly_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly metrics for students.

    Args:
        data (DataFrame): The DataFrame containing student data with date information.

    Returns:
        DataFrame: A DataFrame summarizing the total and graduated students per year.

    Raises:
        KeyError: If the 'Date' or 'End_Date' columns are missing from the DataFrame.
        ValueError: If there are issues with the data's content, format, or calculations.
    """
    # Extract the year from the 'Date' column for each row
    data['Year'] = data['Date'].dt.year

    # Dictionary defining how to aggregate data for each year
    agg_dict: Dict[str, pd.NamedAgg] = {
        'Total_Students': pd.NamedAgg(column='Name', aggfunc='nunique'),  # Count of unique students per year
        'Graduated_Students': pd.NamedAgg(
            column='End_Date',
            aggfunc=lambda x: (x < data['Date'].max()).sum()  # Count of students graduated till the last date in data
        )
    }
    return data.groupby('Year').agg(**agg_dict)
