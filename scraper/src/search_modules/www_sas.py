from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    students = []
    
    # Find all articles containing information about individuals
    articles = source.find_all('article')
    
    # Iterate over each article to extract PhD student names
    for article in articles:
        position = article.find('p', class_='position')
        if position and position.text == 'PhD':
            name = article.find('h4', class_='name')
            if name:
                full_name = name.text.strip()
                match = re.match(r'(\w+),\s*(\w+)', full_name)
                if match:
                    first_name, last_name = match.groups()
                    corrected_name = f'{first_name} {last_name}'
                    students.append(corrected_name)
    
    return students
