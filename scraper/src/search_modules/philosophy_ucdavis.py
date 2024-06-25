from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    articles = source.find_all('article', class_='node node--type-sf-person vm-teaser--grouped vm-teaser')
    
    for article in articles:
        position = article.find('ul', class_='vm-teaser__position')
        
        if position:
            position_text = position.find('li', class_='field__item').get_text(strip=True)
            if position_text == 'Graduate Student':
                title = article.find('h3', class_='vm-teaser__title').find('span', class_='field--name-title').get_text(strip=True)
                students.append(title)
    
    return students
