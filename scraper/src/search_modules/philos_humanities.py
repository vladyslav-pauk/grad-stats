from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    profile_items = source.find_all('div', class_='profile-item-info')
    
    for item in profile_items:
        program = item.find('div', class_='profile-item--program').text
        position = item.find('div', class_='profile-item--position').text
        
        if 'PhD' in program and 'Current Students' in position:
            name = item.find('div', class_='profile-item--name').text.strip()
            student_names.append(name)
    
    return student_names
