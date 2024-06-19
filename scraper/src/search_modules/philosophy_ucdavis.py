from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    student_articles = source.find_all('article', class_='node--type-sf-person')
    for article in student_articles:
        position = article.find('ul', class_='vm-teaser__position')
        if position and 'Graduate Student' in position.text:
            name_element = article.find('span', class_='field--name-title')
            if name_element:
                phd_students.append(name_element.text.strip())
    return phd_students
