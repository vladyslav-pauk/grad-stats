from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    student_list = source.select('div.content p.title.small:contains("Graduate Student")')
    
    for student in student_list:
        name = student.find_previous('h1').text
        students.append(name)
    
    return students
