from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []

    student_elements = source.find_all('div', class_='entry-content')
    
    for student_element in student_elements:
        name_elements = student_element.find_all('h3')

        for name_element in name_elements:
            students.append(name_element.text.strip())

    return students
