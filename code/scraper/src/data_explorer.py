import pickle

import pandas as pd

path_to_dataset = '/Users/studio/Work/Projects/Education/code/'
latest_data_path = f'{path_to_dataset}dataset/student_data_v2.pkl'

with open(latest_data_path, "rb") as f:
    df = pickle.load(f)

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(df['Snapshots'].apply(lambda x: len(x)))
