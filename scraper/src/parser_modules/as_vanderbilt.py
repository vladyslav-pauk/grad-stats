from bs4 import BeautifulSoup
import re

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    name_pattern = re.compile(r"[A-Za-z -]+")
    names = set()
    
    for strong_tag in source.find_all("strong"):
        name = strong_tag.get_text()
        if name_pattern.fullmatch(name):
            names.add(name)
    
    return list(names)
