"""
This module provides functions to fetch Wayback Machine snapshots for a given URL with a retry mechanism.

Functions:
    get_snapshot_urls(url_tuple: Tuple[str], max_retries: int, retry_delay: int, log: bool = False) -> List[str]:
        Fetches a list of Wayback Machine snapshots for a given URL with retry logic.

    _match_urls(response_text: str) -> List[str]:
        Extracts snapshot URLs from the Wayback Machine API response.
"""

import requests
import logging
from typing import Tuple, List

from requests.exceptions import ConnectionError, HTTPError, Timeout

from .exceptions import handle_retry_exception


def get_snapshot_urls(
        url_tuple: Tuple[str, str, str],
        max_retries: int = 10,
        retry_delay: int = 16,
        log: bool = False
) -> List[str]:
    """
    Fetches a list of Wayback Machine snapshots for a given URL with a retry mechanism.

    Args:
        url_tuple (Tuple[str]): A tuple containing the URL to fetch snapshots for.
        max_retries (int): Maximum number of retries on a failed request. Default is 10.
        retry_delay (int): Initial delay in seconds between retries. Default is 16.
        log (bool): If True, logs the number of snapshots found.

    Returns:
        List[str]: A list of snapshot URLs. Returns an empty list if an error occurs.
    """
    timegate_url = 'http://web.archive.org/web/timemap/link/'
    attempts = 0

    url, placement_url = (url_tuple + (None,) * 2)[:2]

    while attempts < max_retries:
        try:
            response = requests.get(timegate_url + url)
            response.raise_for_status()
            snapshot_urls = _match_urls(response.text)
            snapshot_urls.append(url)

            if log:
                logging.info(
                    f"Found {len(snapshot_urls)} archive snapshot{'s' if len(snapshot_urls) > 1 else ''}")
            return snapshot_urls

        except (HTTPError, ConnectionError, Timeout) as e:
            retry_delay, attempts = handle_retry_exception(e, attempts, retry_delay)

    else:
        logging.error(f"Failed to fetch snapshots after {max_retries} attempts")
        return [url_tuple[0]]


def _match_urls(response_text: str) -> List[str]:
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
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     url_to_check = "http://example.com"
#     snapshots = get_snapshot_urls(url_to_check, log=True)
#     print(snapshots)
