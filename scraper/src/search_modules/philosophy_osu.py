from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_student_names = []
    
    students = source.find_all('a', class_='views-field-field-first-name')

    for student in students:
        phd_student_names.append(student.text)
    
    return phd_student_names
