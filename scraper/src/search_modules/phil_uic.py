from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    student_blocks = source.find_all('h3', class_='_title')
    
    for block in student_blocks:
        span_academic_title = block.find('span', class_='_academic-title')
        if span_academic_title and span_academic_title.text.strip() == 'Graduate Student':
            name = block.find('span', class_='_name').text.strip()
            formatted_name = re.sub(r'[,\s]+', ' ', name)  # Replace multiple spaces and commas with a single space
            students.append(formatted_name)
    
    return students
