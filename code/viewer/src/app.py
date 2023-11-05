import os
import pickle
import sys
from datetime import datetime

from flask import Flask, render_template, request, Markup
from ydata_profiling import ProfileReport

sys.path.append('/Users/studio/Work/Projects/Education/code/')
from scraper.src.utils import get_latest_version

app = Flask(__name__, template_folder='../templates', static_folder='../static')

def read_latest_data(url, path_to_dataset='/Users/studio/Work/Projects/Education/code/'):
    latest_version = get_latest_version()
    latest_data_path = f'{path_to_dataset}dataset/student_data_v{latest_version}.pkl'
    if os.path.exists(latest_data_path):
        with open(latest_data_path, "rb") as f:
            df = pickle.load(f)
        filtered_data = df[df['URL'] == url]
        snapshots = filtered_data['Snapshots'].tolist()
        return filtered_data, snapshots
    else:
        return None, None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            result, _ = read_latest_data(url)
            if result is not None:
                result.drop(['Email', 'URL'], axis=1, inplace=True)
                # result['Snapshots'] = result['Snapshots'].apply(lambda x: len(x))
                result['Start_Date'] = result['Start_Date'].astype(str)
                result['End_Date'] = result['End_Date'].astype(str)
                profile = ProfileReport(result, title="Profiling Report")
                result_html = profile.to_html()
                result_safe_html = Markup(result_html)
                snapshot_dates = []
                snapshots = result['Snapshots'].iloc[0].tolist()
                for snap in snapshots:
                    if '/web/' in snap:
                        date_str = snap.split('/web/')[1].split('/')[0][:-6]  # Remove HMS
                        date_formatted = datetime.strptime(date_str, "%Y%m%d").strftime("%m/%d/%Y")
                    else:
                        date_formatted = datetime.now().strftime("%m/%d/%Y")
                    snapshot_dates.append({'url': snap, 'date': date_formatted})

                return render_template("index.html", result=result_safe_html, snapshot_dates=snapshot_dates, error=None)
            else:
                return render_template("index.html", result=None, error="No matching data found.")
        except Exception as e:
            return render_template("index.html", result=None, error=f"Please enter a valid URL.")
    return render_template("index.html", result=None, snapshot_dates=[], error=None)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
