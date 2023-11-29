import re
import pandas as pd
import logging


def process_data(data):
    student_info = pd.DataFrame(index=data['Name'].unique(), columns=[
        'Snapshots',
        'University', 'Department', 'URL', 'Start_Date', 'End_Date', 'Years', 'Active'])

    for name in student_info.index:
        student_data = data[data['Name'] == name]
        student_info.loc[name, ['University', 'Department']] = student_data.iloc[0][['University', 'Department']]
        student_info.at[name, 'URL'] = clean_url(student_data['URL'].iloc[0])
        student_info.at[name, 'Start_Date'] = pd.to_datetime(student_data['Date'].min()).date()
        student_info.at[name, 'End_Date'] = pd.to_datetime(student_data['Date'].max()).date()
        student_info.at[name, 'Years'] = (student_info.at[name, 'End_Date'] - student_info.at[name, 'Start_Date']).days / 365.25
        student_info.at[name, 'Active'] = student_data['Active'].sum() > 0
        student_info.at[name, 'Snapshots'] = student_data['URL'].unique().tolist()

    appearance_data = student_info.reset_index().rename(columns={'index': 'Name'})

    logging.info(f"Found {len(appearance_data)} new candidates.")

    return appearance_data


def clean_url(url):
    match = re.search(r'https?://web\.archive\.org/web/\d+/(https?://.+)', url)
    return match.group(1) if match else url


def calculate_yearly_metrics(data):
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    agg_dict = {
        'Total_Students': pd.NamedAgg(column='Name', aggfunc='nunique'),
        'Graduated_Students': pd.NamedAgg(
            column='End_Date',
            aggfunc=lambda x: (x < pd.Timestamp(data['Date'].max())).sum()
        )
    }
    return data.groupby('Year').agg(**agg_dict)
