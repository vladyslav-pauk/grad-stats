from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    student_divs = source.find_all('div', class_='views-row')
    
    for student_div in student_divs:
        student_info = student_div.find('div', class_='views-field-title')
        student_name = student_info.find('a').text
        phd_students.append(student_name)
    
    return phd_students
