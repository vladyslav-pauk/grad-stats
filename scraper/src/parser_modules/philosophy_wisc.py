from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    pattern = re.compile(r"\b[A-Za-z -]+\b")
    names = set()
    
    for h3 in source.find_all("h3"):
        match = pattern.search(h3.text)
        if match:
            names.add(match.group().strip())
    
    return list(names)
