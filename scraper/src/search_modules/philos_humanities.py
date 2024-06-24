from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_student_names = []
    
    profiles = source.find_all("div", class_="profile-item")
    
    for profile in profiles:
        program = profile.find("div", class_="profile-item--program")
        if program and "PhD" in program.text:
            name = profile.find("div", class_="profile-item--name")
            if name:
                phd_student_names.append(name.text.strip())
    
    return phd_student_names
