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
    elif 'ucdavis.edu' in url:
        return extract_names_ucdavis(soup)
    elif 'ucsb.edu' in url:
        return extract_names_ucsb(soup)
    elif 'ucsc.edu' in url:
        return extract_names_ucsc(soup)
    elif 'uic.edu' in url:
        return extract_names_uic(soup)
    elif 'stonybrook.edu' in url:
        return extract_names_stonybrook(soup)
    elif 'nyu.edu' in url:
        return extract_names_nyu(soup)
    elif 'princeton.edu' in url:
        return extract_names_princeton(soup)
    elif 'tamu.edu' in url:
        return extract_names_tamu(soup)
    elif 'osu.edu' in url:
        return extract_names_osu(soup)
    elif 'jhu.edu' in url:
        return extract_names_jhu(soup)
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


def extract_names_ucdavis(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all h3 tags with the 'vm-teaser__title' class
    h3_tags = soup.find_all('h3', class_='vm-teaser__title')
    for h3 in h3_tags:
        span_tag = h3.find('span', class_='field field--name-title field--type-string field--label-hidden')
        if span_tag and span_tag.text.strip():
            names.append(span_tag.text.strip())

    return names, 'UC Davis', 'Philosophy'


def extract_names_ucsb(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all span tags with the 'field-content' class
    span_tags = soup.find_all('span', class_='field-content')
    for span in span_tags:
        a_tag = span.find('a')
        if a_tag and a_tag.text.strip():
            names.append(a_tag.text.strip())

    return names, 'UC Santa Barbara', 'Philosophy'


def extract_names_ucsc(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all span tags with the 'p-name' class
    span_tags = soup.find_all('span', class_='p-name')
    for span in span_tags:
        if span and span.text.strip():
            names.append(span.text.strip())

    # Additional scenario: Find all h3 tags within a tags, nested inside td tags
    td_tags = soup.find_all('td', colspan="2")
    for td in td_tags:
        h3_tag = td.find('h3')
        if h3_tag and h3_tag.text.strip():
            names.append(h3_tag.text.strip())

    return names, 'UC Santa Cruz', 'Philosophy'


def extract_names_uic(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all h3 tags with the '_title' class
    h3_tags = soup.find_all('h3', class_='_title')
    for h3 in h3_tags:
        span_tag = h3.find('span', class_='_name')
        if span_tag:
            a_tag = span_tag.find('a')
            if a_tag and a_tag.text.strip():
                names.append(a_tag.text.strip())

    names = [name.replace('\n', '').strip() for name in names]
    names = [name.split(',')[1].strip() + ' ' + name.split(',')[0].strip() for name in names]

    return names, 'University of Illinois Chicago', 'Philosophy'


def extract_names_stonybrook(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all h3 tags
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        if h3 and h3.text.strip():
            names.append(h3.text.strip())

    return names, 'Stony Brook University', 'Philosophy'


def extract_names_nyu(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all h5 tags and extract names from nested a tags
    h5_tags = soup.find_all('h5')
    for h5 in h5_tags:
        a_tag = h5.find('a')
        if a_tag and a_tag.text.strip():
            names.append(a_tag.text.strip())

    return names, 'New York University', 'Philosophy'


def extract_names_princeton(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Define the phrases to filter out
    filter_phrases = ["Princeton University", "Department of Philosophy"]

    # Find all img tags and extract names from the alt attribute
    img_tags = soup.find_all('img')
    for img in img_tags:
        alt_text = img.get('alt', '').strip()
        # Check and exclude the filter phrases
        if alt_text and not any(filter_phrase in alt_text for filter_phrase in filter_phrases):
            names.append(alt_text)

    return names, 'Princeton University', 'Philosophy'


def extract_names_tamu(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all span tags with the 'name' class and extract names from nested a tags
    span_tags = soup.find_all('span', class_='name')
    for span in span_tags:
        a_tag = span.find('a')
        if a_tag and a_tag.text.strip():
            names.append(a_tag.text.strip())

    print(names)
    return names, 'Texas A&M University', 'Philosophy'


def extract_names_osu(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Find all span tags with the 'field-content' class and extract names from the title attribute of nested a tags
    span_tags = soup.find_all('span', class_='field-content')
    for span in span_tags:
        a_tag = span.find('a')
        if a_tag and a_tag.get('title', '').strip():
            names.append(a_tag['title'].strip())

    return names, 'Ohio State University', 'Philosophy'


def extract_names_jhu(soup: BeautifulSoup) -> Tuple[List[str], str, str]:
    names = []

    # Define the phrases to filter out
    filter_phrases = ["Logo: Johns Hopkins University", "Home"]

    # Find all img tags and extract names from the alt attribute
    img_tags = soup.find_all('img')
    for img in img_tags:
        alt_text = img.get('alt', '').strip()
        # Check and exclude the filter phrases
        if alt_text and not any(filter_phrase in alt_text for filter_phrase in filter_phrases):
            names.append(alt_text)

    return names, 'Johns Hopkins University', 'Philosophy'