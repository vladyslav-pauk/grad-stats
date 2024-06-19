from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    # Find all elements with the class "field__item" to identify Ph.D. students
    phd_students = source.find_all(class_="field__item")

    for student in phd_students:
        if "Ph.D. Student" in student.get_text() and "Graduate Teaching Assistant" in student.get_text():  # Ensure both Ph.D. Student and GTA status is present
            student_info = student.find_parent(class_="field__items")
            student_name = student_info.find(class_="field--name-title").get_text().strip()
            students.append(student_name)
    
    return students
