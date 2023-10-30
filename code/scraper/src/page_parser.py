import datetime
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in self.soup(['script', 'style']):
            script_or_style.extract()

        self.status = False
        try:
            self.date = pd.to_datetime(url.split('/web/')[1].split('/')[0])
            path_elements = urlparse(url).path.split('.')
        except IndexError:
            self.date = pd.to_datetime(datetime.datetime.today())
            self.status = True
            path_elements = urlparse(url).netloc.split('.')

        self.university_name = path_elements[1] if len(path_elements) > 1 else None
        self.department_name = path_elements[0].split("/")[-1] if len(path_elements) > 1 else None
        # fixme: universities, departments - web.engineering.arizona.edu vs eller.arizona.edu
        self.url = url
        # fixme: collect url without webmaster//

    def extract_info(self):
        page_data = pd.DataFrame()

        mailto_elements = self.soup.find_all(href=lambda x: x and 'mailto:' in x)
        # fixme: duplicate emails:
        #  saffo@arizona.edu	  3
        #  saffo@ema

        for mailto in mailto_elements:
            email = mailto.get_text().strip()
            if email:
                new_row = pd.DataFrame({
                    'Email': [email],
                    'University': [self.university_name],
                    'Department': [self.department_name],
                    'URL': [self.url],
                    'Date': [self.date],
                    'Status': [self.status]
                })
                page_data = pd.concat([page_data, new_row], ignore_index=True)

        return page_data
