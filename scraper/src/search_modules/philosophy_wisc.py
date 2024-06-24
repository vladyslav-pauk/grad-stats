from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    faculty_members = source.find_all('div', class_='faculty-member')
    
    for faculty_member in faculty_members:
        faculty_name = faculty_member.find('h3', class_='faculty-name')
        if faculty_name:
            phd_students.append(faculty_name.text.strip())
    
    return phd_students
