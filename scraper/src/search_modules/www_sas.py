from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    
    articles = source.find_all('article')  # Find all <article> tags
    
    for article in articles:
        # Check if the article contains information about a PhD student
        if article.find('p', class_='position') and article.find('p', class_='position').text == 'PhD':
            student_name = article.find('h4', class_='name').text
            phd_students.append(student_name)
    
    return phd_students
