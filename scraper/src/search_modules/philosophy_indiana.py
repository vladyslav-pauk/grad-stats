from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    
    articles = source.find_all("article", {"class": "profile item ok"})
    
    for article in articles:
        title = article.find("p", class_="title small")
        if title and "Graduate Student" in title.text:
            student_name = article.find("h1", class_="no-margin").text
            phd_students.append(student_name)
    
    return phd_students
