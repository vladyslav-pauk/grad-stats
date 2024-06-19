from bs4 import BeautifulSoup

def extract_phd_student_names(soup: BeautifulSoup) -> list[str]:
    phd_students = []

    # Find the section where the student details are located
    students_section = soup.find('div', {'class': 'secmain'})
    
    if students_section:
        # Extract names and add them to the list
        for student_info in students_section.find_all('strong'):
            student_name = student_info.get_text()
            phd_students.append(student_name)
    
    return phd_students
