import logging

import requests


def get_snapshots(url, log=False):
    timegate_url = 'http://web.archive.org/web/timemap/link/'
    response = requests.get(timegate_url + url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve snapshots. HTTP Status Code: {response.status_code}")
        return [url]
    link_header = response.text.strip().split('\n')
    snapshots = [link.split(';')[0].strip('<>') for link in link_header if 'rel="memento"' in link]
    snapshots.append(url)
    if log:
        logging.info(f"Found {len(snapshots)} snapshots for {url}")

    return snapshots
