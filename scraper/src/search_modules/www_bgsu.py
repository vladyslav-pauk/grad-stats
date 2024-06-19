from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    phd_students_section = source.find('li', class_='cmp-sidenav__child cmp-sidenav__item active')
    if phd_students_section:
        student_name_tags = phd_students_section.find_all('a', class_='cmp-sidenav__child-link cmp-sidenav__child-link--active')
        students = [student_name_tag.text for student_name_tag in student_name_tags]
    
    return students
