from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    names = []
    student_cards = source.find_all('li', class_='profile-listing-card')
    
    for card in student_cards:
        student_name = card.find('h3').text
        names.append(student_name)
    
    return names
