from flask import Flask
from .views import index, search_urls, fetch_all_data, programs, about
import logging


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.

    Args:
        test_config (dict, optional): A configuration dictionary to use for testing.
                                      Defaults to None, which means the app will be configured
                                      based on the production settings.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Setup URL routes
    app.add_url_rule('/about', view_func=about, methods=["GET"])
    app.add_url_rule('/', view_func=index, methods=["GET", "POST"])
    app.add_url_rule('/programs', view_func=programs, methods=["GET", "POST"])
    app.add_url_rule('/search-urls', view_func=search_urls, methods=["GET"])
    app.add_url_rule('/fetch-all-data', view_func=fetch_all_data, methods=["GET"])

    return app
