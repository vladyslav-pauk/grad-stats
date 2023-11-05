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

        # fixme: universities, departments - web.engineering.arizona.edu vs eller.arizona.edu
        # fixme: collect url without webmaster//
        # fixme: duplicate emails:
        #  saffo@arizona.edu	  3
        #  saffo@ema
        # fixme: pages without emails

    def extract_info(self):
        page_data = pd.DataFrame()

        mailto_elements = self.filter_mailto_elements(self.soup.find_all(href=lambda x: x and 'mailto:' in x))

        for mailto in mailto_elements:
            email, name = self.extract_emails_and_names(mailto)
            if email and name:
                new_row = self.create_data_entry(email, name)
                page_data = pd.concat([page_data, new_row], ignore_index=True)

        return page_data

    def filter_mailto_elements(self, mailto_elements):
        generic_terms = self.get_generic_terms()
        return [el for el in mailto_elements if not self.filter_email_prefix(el.get_text(), generic_terms)]

    def extract_emails_and_names(self, mailto):
        email = mailto.get_text().strip()
        name = self.find_name_closest_to_email(mailto, email)
        return email, name

    def filter_email_prefix(self, email, generic_terms):
        email_prefix = email.split('@')[0].lower()
        return any(generic_term in email_prefix for generic_term in generic_terms)

    def create_data_entry(self, email, name):
        return pd.DataFrame({
            'Email': [email],
            'Name': [name],
            'University': [self.university_name],
            'Department': [self.department_name],
            'URL': [self.url],
            'Date': [self.date],
            'Active': [self.status]
        })

    def find_name_closest_to_email(self, mailto_element, email):
        surrounding_text = self.get_surrounding_text(mailto_element)
        potential_names = self.find_potential_names(surrounding_text + self.soup.get_text())
        return self.match_name_with_email(email, potential_names)

    def get_surrounding_text(self, mailto_element):
        # This method is simplified; you might want to include additional logic here
        return mailto_element.find_parent().text

    def find_potential_names(self, text):
        return re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)

    def match_name_with_email(self, email, potential_names):
        email_prefix = email.split('@')[0]
        best_match, highest_score = None, 0
        for name in potential_names:
            score = SequenceMatcher(None, email_prefix.lower(), name.replace(' ', '').lower()).ratio()
            if score > highest_score:
                highest_score = score
                best_match = name
        return best_match if best_match else 'Unknown'

    def get_generic_terms(self):
        generic_terms = {'contact', 'info', 'support', 'admin', 'webmaster', 'reply'}
        university_department_terms = set()
        if self.university_name:
            university_department_terms.update(re.split(r'\W+', self.university_name.lower()))
        if self.department_name:
            university_department_terms.update(re.split(r'\W+', self.department_name.lower()))
        additional_generic_terms = {'university', 'college', 'school', 'institute', 'department', 'faculty', 'staff',
                                    'directory', 'student'}
        generic_terms.update(university_department_terms)
        generic_terms.update(additional_generic_terms)
        return generic_terms


# Example usage:
url = "https://ischool.arizona.edu/phd-students"
parser = PageParser(url)
page_data = parser.extract_info()
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(page_data)
