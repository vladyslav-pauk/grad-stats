from flask import render_template, request, jsonify, Markup
from ydata_profiling import ProfileReport
from .models import get_snapshot_dates, get_latest_data_path, load_dataframe


def programs():
    """
    Renders the main page of the application. Handles the form submissions for URL input
    and generates profiling reports and snapshot dates for the input URL.

    Returns:
        Rendered HTML for the index page.
    """
    error = None
    result_safe_html = None
    snapshot_dates = []
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            try:
                data_path = get_latest_data_path('dataset')
                df = load_dataframe(data_path)
                if df is not None and url in df['URL'].values:
                    university = df[df['URL'] == url]['University'].iloc[0]
                    df_filtered = df[df['URL'] == url].drop(['Snapshots', 'URL', 'Department', 'University', 'Name'], axis=1)
                    df_filtered = df_filtered[['Active', 'Placement', 'Years', 'Start_Date', 'End_Date']]
                    df_filtered['Start_Date'] = df_filtered['Start_Date'].dt.year.astype(int)
                    df_filtered['End_Date'] = df_filtered['End_Date'].dt.year.astype(int)
                    df_filtered['Years'] = df_filtered['Years'].apply(lambda x: round(x * 4) / 4)
                    profile = ProfileReport(df_filtered,
                                            title=f"Report for {university}",
                                            duplicates=None,
                                            correlations=None,
                                            missing_diagrams=None,
                                            interactions=None,
                                            samples=None,
                                            variables={
                                                "descriptions": {
                                                    "Active": "Indicates whether a student is currently enrolled in the program.",
                                                    "Placement": "Indicates whether a student is in an academic or industry placement.",
                                                    "Years": "Number of years spent in the program.",
                                                    "Start_Date": "Year a student entered the program.",
                                                    "End_Date": "Year a student left the program."
                                                }
                                            })
                    result_safe_html = Markup(profile.to_html())
                    snapshot_dates = get_snapshot_dates(df, url)
                else:
                    error = "No matching data found."
            except Exception as e:
                error = f"An error occurred: {e}"
        else:
            error = "Please enter a valid URL."

    return render_template("programs.html", result=result_safe_html, snapshot_dates=snapshot_dates, error=error)


def search_urls():
    """
    Responds to URL search queries with a list of matching URLs in JSON format.

    Returns:
        JSON response containing a list of matching URLs.
    """
    query = request.args.get('query', '').lower()
    try:
        data_path = get_latest_data_path('dataset')
        df = load_dataframe(data_path)
        if df is not None:
            matching_urls = df[df['URL'].str.lower().str.contains(query)]['URL'].drop_duplicates().tolist()
            return jsonify(matching_urls)
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)})


def fetch_all_data():
    try:
        data_path = get_latest_data_path('dataset')
        df = load_dataframe(data_path)
        df = df.drop(['Snapshots', 'URL', 'Department', 'Name'], axis=1)
        df = df[['University', 'Active', 'Placement', 'Years', 'Start_Date', 'End_Date']]
        df['Start_Date'] = df['Start_Date'].dt.year
        df['End_Date'] = df['End_Date'].dt.year
        df['Years'] = df['Years'].apply(lambda x: round(x * 4) / 4)
        if df is not None:
            profile = ProfileReport(df,
                                    title="Dataset Statistics",
                                    duplicates=None,
                                    correlations=None,
                                    missing_diagrams=None,
                                    interactions=None,
                                    samples=None,
                                    variables={
                                        "descriptions": {
                                            "Active": "Indicates whether a student is currently enrolled in the program.",
                                            "Placement": "Indicates whether a student is in an academic or industry placement.",
                                            "Years": "Number of years spent in the program.",
                                            "Start_Date": "Year a student entered the program.",
                                            "End_Date": "Year a student left the program."
                                        }
                                    })
            profile_html = profile.to_html()
            return jsonify({"profile": profile_html})
        else:
            return jsonify({"error": "No data found."})
    except Exception as e:
        return jsonify({"error": str(e)})


def index():
    return render_template('index.html')


def about():
    """
    Renders the 'about' page of the application.

    Returns:
        Rendered HTML for the about page.
    """
    return render_template("about.html")
