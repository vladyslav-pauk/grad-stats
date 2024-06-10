from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    names = set()
    for h3_tag in source.find_all('h3', class_='cla-people-name'):
        name = h3_tag.get_text().strip()
        # Check if name contains only letters, spaces, and hyphens
        if re.match(r'^[a-zA-Z\s\-]+$', name):
            names.add(name)
    return list(names)
