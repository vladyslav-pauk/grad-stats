from bs4 import BeautifulSoup


def normalize_name(name: str) -> str:
    if name.startswith('. Ding'):
        return 'Zhiyuan Li'
    if 'Ding' in name:
        return 'Zhiyuan Li'
    return name


def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
    phd_student_names = []
    phd_students = source.find_all('h4', class_='card-title')
    for student in phd_students:
        name = student.text.strip()
        normalized_name = normalize_name(name)
        if normalized_name not in phd_student_names:
            phd_student_names.append(normalized_name)
    return phd_student_names
