from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    
    # Find all elements with the class profile-item--position containing "Current Students"
    student_items = source.find_all(class_="profile-item--position", text="Current Students")
    
    # Extract the names of the current PhD students
    for item in student_items:
        name = item.find_previous(class_="profile-item--name").get_text().strip()
        student_names.append(name)
    
    return student_names
