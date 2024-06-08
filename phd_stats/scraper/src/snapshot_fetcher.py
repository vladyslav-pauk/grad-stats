import requests
from requests.exceptions import ConnectionError, HTTPError
import logging
import time


def get_snapshots(url: str, log: bool = False, max_retries: int = 5, retry_delay: int = 60) -> list:
    """
    Fetches a list of Wayback Machine snapshots for a given URL with retry mechanism.

    Args:
        url (str): The URL for which to fetch snapshots.
        log (bool): If True, logs the number of snapshots found.
        max_retries (int): Maximum number of retries on failed request.
        retry_delay (int): Delay in seconds between retries.

    Returns:
        list: A list of snapshot URLs. Returns an empty list if an error occurs.

    Raises:
        HTTPError: If an HTTP error occurs (e.g., the server returned 4XX or 5XX responses).
        Exception: For other types of exceptions that are not specifically network or HTTP errors.
    """
    timegate_url = 'http://web.archive.org/web/timemap/link/'
    attempts = 0

    while attempts < max_retries:
        try:
            response = requests.get(timegate_url + url)
            response.raise_for_status()
            snapshots = extract_snapshots(response.text)
            snapshots.append(url)

            if log:
                logging.info(f"Found {len(snapshots)} snapshots for {url}")

            return snapshots

        except ConnectionError as e:
            logging.error(f"Retrying in {retry_delay}s - Network error: Unable to connect to {timegate_url}")
            attempts += 1
            time.sleep(retry_delay)
        except HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return []

    logging.error(f"Failed to fetch snapshots from {url} after {max_retries} attempts.")
    return []


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
