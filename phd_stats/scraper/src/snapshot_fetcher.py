import requests
from requests.exceptions import ConnectionError


def get_snapshots(url, log=False):
    timegate_url = 'http://web.archive.org/web/timemap/link/'

    try:
        response = requests.get(timegate_url + url)
        response.raise_for_status()  # Check for HTTP request errors
    except ConnectionError:
        print(f"Network error: Unable to connect to {timegate_url}. Please check your network connection.")
        return [url]
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return [url]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [url]

    # Process the response if no exceptions are raised
    link_header = response.text.strip().split('\n')
    snapshots = [link.split(';')[0].strip('<>') for link in link_header if 'rel="memento"' in link]
    snapshots.append(url)

    if log:
        print(f"Found {len(snapshots)} snapshots for {url}")

    return snapshots
