import logging

import requests


class SnapshotFetcher:
    def __init__(self, url):
        self.url = url

    def get_snapshots(self, log=False):
        timegate_url = 'http://web.archive.org/web/timemap/link/'
        response = requests.get(timegate_url + self.url)
        if response.status_code != 200:
            logging.error(f"Failed to retrieve snapshots. HTTP Status Code: {response.status_code}")
            return [self.url]
        link_header = response.text.strip().split('\n')
        snapshots = [link.split(';')[0].strip('<>') for link in link_header if 'rel="memento"' in link]
        snapshots.append(self.url)
        if log:
            logging.info(f"Found {len(snapshots)} snapshots for {self.url}")

        # date = pd.to_datetime(datetime.datetime.today())
        # snapshots.append(str(f"http://web.archive.org/web/{date.strftime('%Y%m%d%H%M%S')}/" + self.url))
        return snapshots

# todo: add __main__ logic
