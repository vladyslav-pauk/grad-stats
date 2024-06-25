from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    student_tags = source.find_all('h3')  # Assuming PhD student names are enclosed in <h3> tags
    for tag in student_tags:
        student_name = tag.text.strip()
        # Removing extra spaces and line breaks
        student_name = ' '.join(student_name.split())
        students.append(student_name)
    
    return students
