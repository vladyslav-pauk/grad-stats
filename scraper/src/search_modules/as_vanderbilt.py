from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    # List to hold the names of PhD students
    phd_student_names = []
    
    # We assume that each PhD student's name is wrapped in a <strong> tag within a <td> with class "biolink"
    # Retrieving all such <td> elements
    student_entries = source.find_all("td", class_="biolink")
    
    # Iterate through each entry found
    for entry in student_entries:
        name_tag = entry.find("strong")
        if name_tag:
            phd_student_names.append(name_tag.get_text(strip=True))
    
    return phd_student_names
