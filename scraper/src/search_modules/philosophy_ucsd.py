from bs4 import BeautifulSoup

def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    student_names = []
    
    for listing in source.find_all('li', class_='profile-listing-card'):
        h3_tag = listing.find('h3')
        if h3_tag:
            student_name = h3_tag.text.strip()
            # Check for characters like hyphen and remove any extra spaces
            if '-' in student_name:
                student_name = student_name.split('-')[0].strip()
            student_names.append(student_name)
    
    return student_names
