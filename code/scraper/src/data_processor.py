import re

import pandas as pd


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def apply(self):
        unique_emails = self.data['Email'].unique()
        student_info = pd.DataFrame(index=unique_emails,
                                    columns=[
                                        'Name',  # New column for student names
                                        'University',
                                        'Department',
                                        'URL',
                                        'Start_Date',
                                        'End_Date',
                                        'Years',
                                        'Active',
                                        'Snapshots'  # Column for Snapshot URLs
                                    ])

        for email in unique_emails:
            student_data = self.data[self.data['Email'] == email]
            student_info.loc[email, 'Name'] = student_data['Name'].iloc[0]  # Assuming 'Name' column exists in self.data
            student_info.loc[email, 'University'] = student_data['University'].iloc[0]
            student_info.loc[email, 'Department'] = student_data['Department'].iloc[0]
            raw_url = student_data['URL'].iloc[0]
            match = re.search(r'https?://web\.archive\.org/web/\d+/(https?://.+)', raw_url)
            clean_url = match.group(1) if match else raw_url

            student_info.loc[email, 'URL'] = clean_url
            student_info.loc[email, 'Start_Date'] = pd.to_datetime(student_data['Date'].min()).date()
            student_info.loc[email, 'End_Date'] = pd.to_datetime(student_data['Date'].max()).date()
            student_info.loc[email, 'Years'] = (student_info.loc[email, 'End_Date'] - student_info.loc[
                email, 'Start_Date']).days / 365.25
            student_info.loc[email, 'Active'] = True if student_data[
                                                            'Active'].sum() > 0 else False  # Assuming 'Status' is binary
            student_info.loc[email, 'Snapshots'] = student_data[
                'URL'].unique().tolist()  # Collect unique snapshot URLs per email

        return student_info.reset_index().rename(columns={'index': 'Email'})

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
