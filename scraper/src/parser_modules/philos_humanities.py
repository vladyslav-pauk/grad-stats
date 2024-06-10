from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    names = set()
    
    # Find all elements with class 'profile-item--program' that contain 'PhD'
    phd_elements = source.find_all(class_="profile-item--program", text=re.compile("PhD"))
    
    # Extract the names from the elements
    for element in phd_elements:
        name_element = element.find_previous(class_="profile-item--name")
        if name_element:
            name = name_element.get_text().strip()
            names.add(name)
    
    # Return unique names as a list
    return list(names)
