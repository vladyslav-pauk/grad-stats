from flask import render_template, request, jsonify, Markup
from ydata_profiling import ProfileReport

from models import get_snapshot_dates, get_latest_data_path, load_dataframe


def index():
    error = None
    result_safe_html = None
    snapshot_dates = []
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            data_path = get_latest_data_path('/phd-stats/')
            df = load_dataframe(data_path)
            if df is not None and url in df['URL'].values:
                df_filtered = df[df['URL'] == url].drop(['URL'], axis=1)
                df_filtered['Start_Date'] = df_filtered['Start_Date'].astype(str)
                df_filtered['End_Date'] = df_filtered['End_Date'].astype(str)
                profile = ProfileReport(df_filtered, title="Profiling Report")
                result_safe_html = Markup(profile.to_html())
                snapshot_dates = get_snapshot_dates(df, url)
            else:
                error = "No matching data found."
        else:
            error = "Please enter a valid URL."

    return render_template("index.html", result=result_safe_html, snapshot_dates=snapshot_dates, error=error)


def search_urls():
    query = request.args.get('query', '').lower()
    data_path = get_latest_data_path('/phd-stats/')
    df = load_dataframe(data_path)
    if df is not None:
        matching_urls = df[df['URL'].str.lower().str.contains(query)]['URL'].drop_duplicates().tolist()
        return jsonify(matching_urls)
    return jsonify([])


def about():
    return render_template("about.html")
