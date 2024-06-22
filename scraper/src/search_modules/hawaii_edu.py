from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    student_blocks = source.find_all('h5')
    for block in student_blocks:
        if block.find('a'):  # Check if the 'h5' tag contains an 'a' tag indicating a student
            student_name = block.text.split('<')[0].strip()
            students.append(student_name)

    return students
