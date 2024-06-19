from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []

    # Find all list items with the specified class that contains the student names
    student_items = source.find_all('li', attrs={'class': 'cla-people-list-item', 'data-position-title': 'Graduate Teaching Assistant'})

    for item in student_items:
        # Extract the student name from the h3 tag within the list item
        student_name = item.find('h3', class_='cla-people-name').text.strip()
        student_names.append(student_name)

    return student_names
