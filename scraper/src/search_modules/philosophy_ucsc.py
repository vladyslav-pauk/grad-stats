from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_students = []
    candidates = source.find_all("strong", string="Title")
    
    for candidate in candidates:
        if candidate.find_next("li").string == "PhD Student":
            student_name = candidate.find_previous("h3", class_="item-name").find("span", class_="p-name").get_text()
            phd_students.append(student_name)
            
    return phd_students
