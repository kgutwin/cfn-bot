import re
from os.path import dirname
from bs4 import BeautifulSoup
from urllib.request import urlopen

RELEASE_HISTORY = "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/ReleaseHistory.html"


TRIM_WHITESPACE = re.compile('\s+')
def strip_internal(s):
    return TRIM_WHITESPACE.subn(' ', s)[0]


def absolute_link(href, base=None):
    if base is None:
        base = dirname(RELEASE_HISTORY)
    if not href.startswith('http'):
        href = f"{base}/{href}"
    return href


def get_release_history():
    response = urlopen(RELEASE_HISTORY)
    return response.read()


def get_release_atoms(html):
    soup = BeautifulSoup(html, 'html.parser')

    table_rows = soup.find('div', id='main-col-body').find(
        'div', class_='table').find_all('tr')
    for row in table_rows[1:]:
        change, description, date = row.find_all('td')

        if description.find_all('dl'):
            for deflist in description.find_all('dl'):
                for defterm in deflist.find_all('dt'):
                    first_word = change.text.strip().split()[0]
                    resource = defterm.text.strip()
                    header = f"{first_word} {resource}"
                    try:
                        link = absolute_link(defterm.find('a').get('href'))
                    except AttributeError:
                        link = RELEASE_HISTORY
                    definition = defterm.find_next_sibling('dd')

                    if definition.find('ul') is not None:
                        for list_el in definition.find_all('li'):
                            def_text = strip_internal(list_el.text).strip()
                            yield header, def_text, link, date.text.strip()
                    else:
                        for para in definition.find_all('p'):
                            def_text = strip_internal(para.text).strip()
                            yield header, def_text, link, date.text.strip()
        
        else:
            desc_p = strip_internal(description.find('p').text).strip()
            link = absolute_link(description.find('a').get('href'))
            yield change.text.strip(), desc_p, link, date.text.strip()
