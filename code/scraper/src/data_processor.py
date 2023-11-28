import re
import pandas as pd


def process_data(data):
    student_info = pd.DataFrame(index=data['Email'].unique(), columns=[
        'Name', 'University', 'Department', 'URL', 'Start_Date', 'End_Date',
        'Years', 'Active', 'Snapshots'])

    for email in student_info.index:
        student_data = data[data['Email'] == email]
        student_info.loc[email, ['Name', 'University', 'Department']] = student_data.iloc[0][['Name', 'University', 'Department']]
        student_info.at[email, 'URL'] = clean_url(student_data['URL'].iloc[0])
        student_info.at[email, 'Start_Date'] = pd.to_datetime(student_data['Date'].min()).date()
        student_info.at[email, 'End_Date'] = pd.to_datetime(student_data['Date'].max()).date()
        student_info.at[email, 'Years'] = (student_info.at[email, 'End_Date'] - student_info.at[email, 'Start_Date']).days / 365.25
        student_info.at[email, 'Active'] = student_data['Active'].sum() > 0
        student_info.at[email, 'Snapshots'] = student_data['URL'].unique().tolist()

    return student_info.reset_index().rename(columns={'index': 'Email'})


def clean_url(url):
    match = re.search(r'https?://web\.archive\.org/web/\d+/(https?://.+)', url)
    return match.group(1) if match else url


def calculate_yearly_metrics(data):
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    agg_dict = {
        'Total_Students': pd.NamedAgg(column='Email', aggfunc='nunique'),
        'Graduated_Students': pd.NamedAgg(
            column='End_Date',
            aggfunc=lambda x: (x < pd.Timestamp(data['Date'].max())).sum()
        )
    }
    return data.groupby('Year').agg(**agg_dict)
