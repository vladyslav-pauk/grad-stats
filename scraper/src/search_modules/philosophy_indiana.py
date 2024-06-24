from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    student_list = source.select(".content h1")
    
    for student in student_list:
        students.append(student.text)
        
    return students
