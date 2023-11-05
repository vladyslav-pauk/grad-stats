import datetime
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


# fixme: it misses names without emails, and nicole pagowsky in ischool

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
        self.url = url

    def extract_info(self):
        page_data = pd.DataFrame()

        mailto_elements = self.soup.find_all(href=lambda x: x and 'mailto:' in x)

        generic_terms = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply'}

        # Add university and department names to the set of terms to filter out
        university_department_terms = set()
        if self.university_name:
            university_department_terms.update(re.split(r'\W+', self.university_name.lower()))
        if self.department_name:
            university_department_terms.update(re.split(r'\W+', self.department_name.lower()))

        # Define other generic terms to filter out
        additional_generic_terms = {'university', 'college', 'school', 'institute', 'department',
                                    'faculty', 'staff', 'directory', 'student'}
        generic_terms.update(university_department_terms)
        generic_terms.update(additional_generic_terms)

        for mailto in mailto_elements:
            email = mailto.get_text().strip()
            if email:
                email_prefix = email.split('@')[0].lower()
                # Skip the email if the prefix is generic, contains 'info', or matches university/department names
                if any(generic_term in email_prefix for generic_term in generic_terms):
                    continue
                name = self.find_name_closest_to_email(mailto, email)

                # If the name is None or contains generic/university/department terms, skip it
                if not name or any(term in name.lower() for term in generic_terms):
                    continue
                new_row = pd.DataFrame({
                    'Email': [email],
                    'Name': [name],
                    'University': [self.university_name],
                    'Department': [self.department_name],
                    'URL': [self.url],
                    'Date': [self.date],
                    'Active': [self.status]
                })
                page_data = pd.concat([page_data, new_row], ignore_index=True)

        return page_data

    def find_name_closest_to_email(self, mailto_element, email):
        email_prefix = email.split('@')[0]
        # Get a reasonable range of surrounding text
        surrounding = mailto_element.find_parent().text + mailto_element.find_previous_sibling().text if mailto_element.find_previous_sibling() else mailto_element.find_parent().text
        # Split the text into words and find potential names (two consecutive capitalized words)
        potential_names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', surrounding)

        # Use SequenceMatcher to find the best match
        best_match = None
        highest_score = 0
        for name in potential_names:
            # Simplified comparison, can be improved with more sophisticated heuristics
            score = SequenceMatcher(None, email_prefix.lower(), name.replace(' ', '').lower()).ratio()
            if score > highest_score:
                highest_score = score
                best_match = name

        # If no match found nearby, search the whole document
        if not best_match:
            potential_names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', self.soup.get_text())
            for name in potential_names:
                score = SequenceMatcher(None, email_prefix.lower(), name.replace(' ', '').lower()).ratio()
                if score > highest_score:
                    highest_score = score
                    best_match = name

        return best_match if best_match else 'Unknown'


# Example usage:
url = "https://ischool.arizona.edu/phd-students"
parser = PageParser(url)
page_data = parser.extract_info()
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(page_data)
