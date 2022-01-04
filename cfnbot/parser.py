import re
from os.path import dirname
from bs4 import BeautifulSoup
from urllib.request import urlopen

RELEASE_HISTORY = "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/ReleaseHistory.html"


TRIM_WHITESPACE = re.compile(r'\s+')
def strip_internal(s):
    return TRIM_WHITESPACE.subn(' ', s)[0]


def absolute_link(href, base=None):
    if base is None:
        base = dirname(RELEASE_HISTORY)
    if not href.startswith('http'):
        href = f"{base}/{href}"
    return href

#
# Soup helper functions

def get_table_rows(soup):
    table_rows = soup.find('div', id='main-col-body').find(
        'div', class_='table-contents').find_all('tr')
    for row in table_rows:
        if not row.find('th'):
            yield row.find_all('td')

def get_deflist_pairs(element):
    for deflist in element.find_all('dl'):
        for defterm in deflist.find_all('dt'):
            yield defterm, defterm.find_next_sibling('dd')


def get_link(element):
    try:
        return absolute_link(element.a.get('href'))
    except AttributeError:
        return RELEASE_HISTORY


def only_elements_with_content(els):
    for e in els:
        content = e.string or e.text
        if content.strip():
            yield e
    
    
def get_concatenatable_list(element):
    if not element.text.strip().endswith(':'):
        return

    succ_el = next(iter(only_elements_with_content(element.next_siblings)))
    if succ_el.name == 'ul' or succ_el.find('ul'):
        ul = succ_el
    else:
        return

    list_entries = [e.text.strip() for e in ul.find_all('li')]
    if max(len(i.split()) for i in list_entries) <= 3:
        # They are all single, double or triple words
        return ', '.join(list_entries)
    

def get_release_history():
    response = urlopen(RELEASE_HISTORY)
    return response.read()


def get_release_atoms(html):
    soup = BeautifulSoup(html, 'html.parser')

    for change, description, date in get_table_rows(soup):
        has_deflist = len(description.find_all('dl')) > 0
        
        for defterm, definition in get_deflist_pairs(description):
            first_word = change.text.strip().split()[0]
            resource = defterm.text.strip()
            header = strip_internal(f"{first_word} {resource}")
            link = get_link(defterm)

            children_iterator = iter(
                only_elements_with_content(definition.children))
            for child in children_iterator:
                cl = get_concatenatable_list(child)
                if cl:
                    def_text = strip_internal(child.text.strip() + ' '
                                              + cl).strip()
                    yield header, def_text, link, date.text.strip()
                    next(children_iterator)
                    
                elif child.find_all('li'):
                    for list_el in child.find_all('li'):
                        def_text = strip_internal(list_el.text).strip()
                        yield header, def_text, link, date.text.strip()
                else:
                    def_text = strip_internal(child.text).strip()
                    yield header, def_text, link, date.text.strip()
        
        if not has_deflist:
            header = strip_internal(change.text.strip())
            desc_p = strip_internal(description.find('p').text).strip()
            link = get_link(description)
            yield header, desc_p, link, date.text.strip()
