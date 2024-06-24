from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    
    # Find all <h3> tags within the source
    student_names = source.find_all("h3", class_="cmp-staff-profile-widget__name")
    
    for tag in student_names:
        student_name = tag.text.strip()
        if len(student_name.split()) >= 2:  # Check if name has at least two words
            phd_students.append(student_name)
    
    return phd_students
