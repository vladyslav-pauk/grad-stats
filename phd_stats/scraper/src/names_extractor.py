from bs4 import BeautifulSoup
from typing import List
from typing import Tuple

GENERIC_NAMES = {'Student', 'Ph.D.', 'philosophy', 'education'}


def extract_names(soup: BeautifulSoup, url: str) -> Tuple[List[str], str, str]:
    if 'arizona.edu' in url:
        return extract_names_arizona(soup)
    elif 'bgsu.edu' in url:
        return extract_names_bgsu(soup)
    elif 'indiana.edu' in url:
        return extract_names_indiana(soup)
    elif 'rochester.edu' in url:
        return extract_names_rochester(soup)
    elif 'hawaii.edu' in url:
        return extract_names_hawaii(soup)
    elif 'ucsd.edu' in url:
        return extract_names_ucsd(soup)
    elif 'mcmaster.ca' in url:
        return extract_names_mcmaster(soup)
    elif 'colostate.edu' in url:
        return extract_names_colostate(soup)
    elif 'wisc.edu' in url:
        return extract_names_wisc(soup)
    elif 'vanderbilt.edu' in url:
        return extract_names_vanderbilt(soup)
    else:
        return []


def extract_names_arizona(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    classes_to_search = ['field field--name-title field--type-string field--label-hidden',
                         'rdf-meta element-hidden']
    names = []
    for class_name in classes_to_search:
        name_tags = soup.find_all('span', class_=class_name)
        for tag in name_tags:
            if tag.has_attr('content'):
                name = tag['content']
            else:
                name = tag.text.strip()
            name_parts = name.split()
            if not any(part in GENERIC_NAMES for part in name_parts):
                names.append(name)
    return names, 'University of Arizona', 'Philosophy'


def extract_names_bgsu(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    name_tags = soup.find_all('h3', class_='cmp-staff-profile-widget__name')
    names = [tag.text.strip() for tag in name_tags]
    return names, 'Bowling Green State University', 'Philosophy'


def extract_names_indiana(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    h1_tags = soup.find_all('h1', class_='no-margin')
    names = []
    for tag in h1_tags:
        a_tag = tag.find('a')
        if a_tag and a_tag.text.strip():
            names.append(a_tag.text.strip())
    return names, 'Indiana University', 'Philosophy'


def extract_names_rochester(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    div_elements = soup.find_all('div')
    name_tags = []
    for div in div_elements:
        h4_tags = div.find_all('h4')
        name_tags.extend(h4_tags)
    names = list(set([name_tags.text.strip() for name_tags in name_tags]))
    return names, 'University of Rochester', 'Philosophy'


def extract_names_hawaii(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    h5_tags = soup.find_all('h5')
    names = []
    for h5 in h5_tags:
        class_attr = h5.get('class', [])
        if 'wp-block-heading' in class_attr:
            names.append(h5.text.strip())
        else:
            text = ''.join(h5.stripped_strings)
            if text:
                names.append(text)
    return names, 'University of Hawaii', 'Philosophy'


def extract_names_ucsd(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    profile_listing_cards = soup.find_all('li', class_='profile-listing-card')
    names = []
    for card in profile_listing_cards:
        span = card.find('span', class_='profile-listing-data')
        if span:
            h3_tag = span.find('h3')
            if h3_tag and h3_tag.text.strip():
                names.append(h3_tag.text.strip())
    return names, 'University of California, San Diego', 'Philosophy'


def extract_names_mcmaster(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    name_divs = soup.find_all('div', class_='profile-item--name')
    names = [div.text.strip() for div in name_divs if div.text.strip()]
    return names, 'McMaster University', 'Philosophy'


def extract_names_colostate(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    h3_tags = soup.find_all('h3', class_='cla-people-name')
    names = [h3.text.strip() for h3 in h3_tags if h3.text.strip()]
    return names, 'Colorado State University', 'Philosophy'


def extract_names_wisc(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    # Find all h3 tags with the 'faculty-name' class
    h3_tags = soup.find_all('h3')
    names = []
    for h3 in h3_tags:
        a_tag = h3.find('a')  # Find the a tag within the h3 tag
        if a_tag and a_tag.text.strip():
            names.append(a_tag.text.strip())
    return names, 'University of Wisconsin-Madison', 'Philosophy'


def extract_names_vanderbilt(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []
    a_tags = soup.find_all('a', href=lambda href: href and 'bio' in href)
    names.extend([a.text.strip() for a in a_tags if a.text.strip()])
    td_tags = soup.find_all('td', class_='biolink')
    for td in td_tags:
        strong_tag = td.find('strong')
        if strong_tag and strong_tag.text.strip():
            names.append(strong_tag.text.strip())
    return names, 'Vanderbilt University', 'Philosophy'
