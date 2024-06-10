from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_student_names = set()
    name_pattern = re.compile(r'^[A-Za-z\- ]+$')  # Regular expression pattern to match names

    views_fields = source.find_all(class_='views-field views-field-title')
    for view_field in views_fields:
        name = view_field.find(class_='field-content').text.strip()
        if name_pattern.match(name):
            phd_student_names.add(name)

    return list(phd_student_names)
