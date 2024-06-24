from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    students_container = source.find('article', class_='post-121')
    if students_container:
        student_names = students_container.find_all('h5')
        for name_tag in student_names:
            student_name = name_tag.text.strip()
            if re.match(r'^[A-Za-z]+\s[A-Za-z\.]+\s[A-Za-z]+$', student_name):
                students.append(student_name)

    return students
