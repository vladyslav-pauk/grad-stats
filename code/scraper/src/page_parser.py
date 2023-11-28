import datetime
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    [s.extract() for s in soup(['script', 'style'])]

    date, university, department = extract_url_details(url)
    mailto_elements = [el for el in soup.find_all(href=lambda x: x and 'mailto:' in x) if
                       not filter_email(el.get_text())]
    page_data = pd.DataFrame([extract_email_name(el, url, date, university, department) for el in mailto_elements if
                              extract_email_name(el, url, date, university, department)])
    return page_data


def extract_url_details(url):
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0])
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today())

    path_elements = urlparse(url).path.split('.')
    university = path_elements[1] if len(path_elements) > 1 else None
    department = path_elements[0].split("/")[-1] if len(path_elements) > 1 else None

    return date, university, department


def filter_email(email):
    generic_terms = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply'}
    email_prefix = email.split('@')[0].lower()
    return any(term in email_prefix for term in generic_terms)


def extract_email_name(el, soup, url, date, university, department):
    email = el.get_text().strip()
    surrounding_text = el.find_parent().text + soup.get_text()
    potential_names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', surrounding_text)
    email_prefix = email.split('@')[0]
    best_match = max(potential_names, key=lambda name: SequenceMatcher(None, email_prefix.lower(),
                                                                       name.replace(' ', '').lower()).ratio(),
                     default=None)
    name = best_match
    return {'Email': email, 'Name': name, 'University': university, 'Department': department, 'URL': url, 'Date': date, 'Active': False} if name else None
