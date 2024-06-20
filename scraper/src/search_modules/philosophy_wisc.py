from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    graduate_program_submenu = source.find('ul', class_='sub-menu uw-child-menu')
    if graduate_program_submenu:
        student_items = graduate_program_submenu.find_all('li', class_='menu-item')
        for item in student_items:
            name = item.find('a').get_text().strip()
            if len(name.split()) >= 2:
                students.append(name)
    
    return students
