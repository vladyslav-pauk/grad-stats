from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []

    student_cards = source.find_all('li', class_='profile-listing-card')
    for card in student_cards:
        name = card.find('h3').text.strip()
        if name != 'On Yi Sin':
            students.append(name)

    return students
