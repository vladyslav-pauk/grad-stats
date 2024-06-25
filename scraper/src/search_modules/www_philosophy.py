from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    student_tags = source.find_all(class_="views-row")
    
    for tag in student_tags:
        student_name = tag.find(class_="views-field-title").text.strip()
        student_names.append(student_name)
    
    return student_names
