import datetime
import re
from difflib import SequenceMatcher
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    [s.extract() for s in soup(['script', 'style'])]

    date, university, department = extract_url_details(url)
    mailto_elements = [el for el in soup.find_all(href=lambda x: x and 'mailto:' in x) if
                       not filter_email(el.get_text(), department, university)]

    page_data = []
    for el in mailto_elements:
        email, name = extract_email_name(el, soup)
        page_data.append({
            'Email': email,
            'Name': name,
            'University': university,
            'Department': department,
            'URL': url,
            'Date': date,
            'Active': False
        })

    return pd.DataFrame(page_data)


def extract_url_details(url):
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0])
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today())

    path_elements = url.split('.edu')[0].split("/")[-1].split(".")
    university = path_elements[1]
    department = path_elements[0]

    return date, university, department


def filter_email(email, department, university):
    generic_terms = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply', department, university}
    email_prefix = email.split('@')[0].lower()
    return any(term in email_prefix for term in generic_terms)


def extract_email_name(el, soup):
    email = el.get_text().strip()
    surrounding_text = el.find_parent().text + soup.get_text()
    potential_names = find_names(surrounding_text)
    email_prefix = email.split('@')[0]
    best_match = max(potential_names,
                     key=lambda name: SequenceMatcher(None, email_prefix.lower(),
                                                      name.replace(' ', '').lower()).ratio(),
                     default=None)
    return email, best_match


def find_names(text):
    pattern = (r'\b([A-Z][a-zA-Z]*\.?\s(?:[A-Z]\.\s)?[A-Z][a-zA-Z]+(?:-[A-Z][a-z]+)?(?:\s[A-Z][a-z]+(?:-[A-Z]['
               r'a-z]+)?)?)\b')

    potential_names = re.findall(pattern, text)

    return potential_names
