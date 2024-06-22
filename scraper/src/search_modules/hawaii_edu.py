from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    
    student_elements = source.find_all("h5")
    
    for student_element in student_elements:
        student_name = student_element.text.strip()
        if not any(char.isdigit() for char in student_name):
            student_names.append(student_name)
    
    return student_names
