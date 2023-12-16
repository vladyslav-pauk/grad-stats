from flask import render_template, request, jsonify, Markup
from ydata_profiling import ProfileReport
from models import get_snapshot_dates, get_latest_data_path, load_dataframe


def index():
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
                    df_filtered = df[df['URL'] == url].drop(['Snapshots', 'URL'], axis=1)
                    df_filtered['Start_Date'] = df_filtered['Start_Date'].astype(str)
                    df_filtered['End_Date'] = df_filtered['End_Date'].astype(str)
                    profile = ProfileReport(df_filtered, title="Profiling Report")
                    result_safe_html = Markup(profile.to_html())
                    snapshot_dates = get_snapshot_dates(df, url)
                else:
                    error = "No matching data found."
            except Exception as e:
                error = f"An error occurred: {e}"
        else:
            error = "Please enter a valid URL."

    return render_template("index.html", result=result_safe_html, snapshot_dates=snapshot_dates, error=error)


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


def about():
    """
    Renders the 'about' page of the application.

    Returns:
        Rendered HTML for the about page.
    """
    return render_template("about.html")
