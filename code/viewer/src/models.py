import os
import pickle
import sys
from datetime import datetime

sys.path.append('/Users/studio/Work/Projects/Education/code/')
from scraper.src.utils import get_latest_version


def get_latest_data_path(base_path):
    latest_version = get_latest_version()
    return os.path.join(base_path, 'dataset', f'student_data_v{latest_version}.pkl')


def load_dataframe(data_path):
    if os.path.exists(data_path):
        with open(data_path, "rb") as file:
            return pickle.load(file)
    return None


def get_snapshot_dates(df, url):
    snapshots = df[df['URL'] == url]['Snapshots'].explode().unique()
    snapshot_dates = [{
        'url': snap,
        'date': extract_date_from_url(snap)
    } for snap in sorted(snapshots, reverse=True)]
    return snapshot_dates


def extract_date_from_url(url):
    if '/web/' in url:
        date_str = url.split('/web/')[1].split('/')[0][:-6]  # Remove HMS
        return datetime.strptime(date_str, "%Y%m%d").strftime("%m/%d/%Y")
    else:
        return datetime.now().strftime("%m/%d/%Y")
