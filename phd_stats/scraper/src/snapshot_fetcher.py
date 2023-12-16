import requests
from requests.exceptions import ConnectionError, HTTPError
import logging


def get_snapshots(url: str, log: bool = False) -> list:
    """
    Fetches a list of Wayback Machine snapshots for a given URL.

    Args:
        url (str): The URL for which to fetch snapshots.
        log (bool): If True, logs the number of snapshots found.

    Returns:
        list: A list of snapshot URLs. Returns an empty list if an error occurs.

    Raises:
        ConnectionError: If there is a network problem (e.g., DNS failure, refused connection).
        HTTPError: If an HTTP error occurs (e.g., the server returned 4XX or 5XX responses).
        Exception: For other types of exceptions that are not specifically network or HTTP errors.
    """
    timegate_url = 'http://web.archive.org/web/timemap/link/'

    try:
        response = requests.get(timegate_url + url)
        response.raise_for_status()
    except ConnectionError:
        logging.error(f"Network error: Unable to connect to {timegate_url}. Please check your network connection.")
        return []
    except HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        return []
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []

    snapshots = extract_snapshots(response.text)

    if log:
        logging.info(f"Found {len(snapshots)} snapshots for {url}")

    return snapshots


def extract_snapshots(response_text: str) -> list:
    """
    Extracts snapshot URLs from the Wayback Machine API response.

    Args:
        response_text (str): The API response text.

    Returns:
        list: A list of snapshot URLs.
    """
    link_header = response_text.strip().split('\n')
    return [link.split(';')[0].strip('<>') for link in link_header if 'rel="memento"' in link]


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    url_to_check = "http://example.com"
    snapshots = get_snapshots(url_to_check, log=True)
    print(snapshots)
