import re
from typing import DefaultDict

import html2text
import requests

BASE_URL = (
    'https://www.rtve.es/'
    'contenidos/sala-de-comunicacion/programacion-descargable/'
    '{channel}_{date}.html'
)

SEARCH_TERM = 'JJOO TOKYO'
RATING_TERM = 'SIN CALIFICAR'
channel = 'LA1'
date = '23072021'


def match_search_term(line: str):
    if s := re.search(r'\*\*(.*)\*\*', line):
        if SEARCH_TERM in (text := s.groups()[0].strip()):
            return text


def is_rating(line: str):
    return RATING_TERM in line


def is_blank(line: str):
    return line == ''


url = BASE_URL.format(channel=channel, date=date)
response = requests.get(url)
page = html2text.html2text(response.text)

schedule = DefaultDict(list)
add_details = False

for line in page.split('\n'):
    line = line.strip()
    if not add_details and (heading := match_search_term(line)):
        add_details = True
        continue
    if is_rating(line):
        add_details = False
        continue
    if add_details and not is_blank(line):
        schedule[heading].append(line)

print(schedule)
