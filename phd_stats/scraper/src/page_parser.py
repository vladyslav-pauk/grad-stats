import datetime
import logging
import re
from difflib import SequenceMatcher
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_timestamps(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

    except requests.ConnectionError:
        logging.error("Web Archive HTTP Error: Failed to establish a new connection. "
                      "Please check your internet connection or the URL.")
        quit()
    except requests.Timeout:
        logging.error("Web Archive HTTP Error: The request timed out. Please try again later.")
        quit()

    [s.extract() for s in soup(['script', 'style'])]

    date, university, department, status = extract_metadata(url)
    names = extract_names(soup)

    student_timestamps = [{
            'Name': name,
            'University': university,
            'Department': department,
            'URL': url,
            'Date': date,
            'Active': status
        } for name in names]

    return pd.DataFrame(student_timestamps)


def extract_metadata(url):
    try:
        date = pd.to_datetime(url.split('/web/')[1].split('/')[0])
        status = False
    except IndexError:
        date = pd.to_datetime(datetime.datetime.today())
        status = True

    path_elements = url.split('.edu')[0].split("/")[-1].split(".")
    university = path_elements[1]
    department = path_elements[0]

    return date, university, department, status


def extract_names(soup):
    names = []
    mailto_elements = find_emails(soup)
    for el in mailto_elements:
        email = el.get_text().strip()
        surrounding_text = el.find_parent().text + soup.get_text()
        potential_names = match_name_pattern(surrounding_text)
        email_prefix = email.split('@')[0]
        best_match = max(potential_names,
                         key=lambda name: SequenceMatcher(None, email_prefix.lower(),
                                                          name.replace(' ', '').lower()).ratio(),
                         default=None)
        names.append(best_match)
    return names


def find_emails(soup):
    generic_terms = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply', 'philosophy'}
    filtered_elements = []

    for el in soup.find_all(href=lambda x: x and 'mailto:' in x):
        email = el.get_text().strip()
        email_prefix = email.split('@')[0].lower()
        if not any(term in email_prefix for term in generic_terms):
            filtered_elements.append(el)

    return filtered_elements


def match_name_pattern(text):
    pattern = (r'\b([A-Z][a-zA-Z]*\.?\s(?:[A-Z]\.\s)?[A-Z][a-zA-Z]+(?:-[A-Z][a-z]+)?(?:\s[A-Z][a-z]+(?:-[A-Z]['
               r'a-z]+)?)?)\b')

    potential_names = re.findall(pattern, text)

    return potential_names
