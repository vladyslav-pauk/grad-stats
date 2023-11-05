import re

import pandas as pd


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def apply(self):
        student_info = self.create_student_info_dataframe()
        for email in student_info.index:
            self.process_student_data(student_info, email)
        return student_info.reset_index().rename(columns={'index': 'Email'})

    def create_student_info_dataframe(self):
        unique_emails = self.data['Email'].unique()
        return pd.DataFrame(index=unique_emails, columns=[
            'Name', 'University', 'Department', 'URL', 'Start_Date', 'End_Date',
            'Years', 'Active', 'Snapshots'])

    def process_student_data(self, student_info, email):
        student_data = self.data[self.data['Email'] == email]
        student_info.at[email, 'Name'] = student_data['Name'].iloc[0]
        student_info.at[email, 'University'] = student_data['University'].iloc[0]
        student_info.at[email, 'Department'] = student_data['Department'].iloc[0]
        student_info.at[email, 'URL'] = self.clean_url(student_data['URL'].iloc[0])
        student_info.at[email, 'Start_Date'] = pd.to_datetime(student_data['Date'].min()).date()
        student_info.at[email, 'End_Date'] = pd.to_datetime(student_data['Date'].max()).date()
        student_info.at[email, 'Years'] = self.calculate_years(student_info.at[email, 'Start_Date'],
                                                               student_info.at[email, 'End_Date'])
        student_info.at[email, 'Active'] = self.calculate_active_status(student_data)
        student_info.at[email, 'Snapshots'] = self.collect_unique_snapshots(student_data)

    def clean_url(self, url):
        match = re.search(r'https?://web\.archive\.org/web/\d+/(https?://.+)', url)
        return match.group(1) if match else url

    def calculate_active_status(self, student_data):
        return True if student_data['Active'].sum() > 0 else False

    def collect_unique_snapshots(self, student_data):
        return student_data['URL'].unique().tolist()

    def calculate_years(self, start_date, end_date):
        return (end_date - start_date).days / 365.25

    def calculate_yearly_metrics(self):
        self.data['Year'] = pd.to_datetime(self.data['Date']).dt.year
        agg_dict = {
            'Total_Students': pd.NamedAgg(column='Email', aggfunc='nunique'),
            'Graduated_Students': pd.NamedAgg(
                column='End_Date',
                aggfunc=lambda x: (x < pd.Timestamp(self.data['Date'].max())).sum()
            )
        }
        yearly_metrics = self.data.groupby('Year').agg(**agg_dict)
        return yearly_metrics

# # Example usage:
# if __name__ == "__main__":
#     # Assuming `data` is a DataFrame loaded with the required data.
#     processor = DataProcessor(data)
#     student_info = processor.apply()
#     yearly_metrics = processor.calculate_yearly_metrics()
#     print(student_info)
#     print(yearly_metrics)
