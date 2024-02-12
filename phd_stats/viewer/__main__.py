import os
from src.app import create_app

app = create_app()

if __name__ == "__main__":
    """
    The entry point for running the Flask application. It fetches host and port 
    settings from environment variables, falling back to default values if not found.
    """
    # Fetch host and port from environment variables
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = os.environ.get('FLASK_PORT', 5000)
    app.run(host=HOST, port=PORT)
