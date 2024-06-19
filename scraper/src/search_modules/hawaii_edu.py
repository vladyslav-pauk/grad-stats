from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    
    # Find all elements with class "wp-block-heading" which contains student names
    heading_elements = source.find_all('h5', class_='wp-block-heading')
    
    for element in heading_elements:
        student_names.append(element.text)
    
    return student_names
