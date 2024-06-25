from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_student_names = []
    # Find all elements with class 'cmp-staff-profile-widget__name'
    student_elements = source.find_all('h3', class_='cmp-staff-profile-widget__name')
    
    # Extract the text content from each element
    for element in student_elements:
        student_name = element.get_text()
        phd_student_names.append(student_name)
    
    return phd_student_names
