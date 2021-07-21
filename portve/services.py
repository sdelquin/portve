import re

from portve import config


def match_search_term(line: str, search_terms: list = config.SEARCH_TERMS):
    if s := re.search(r'\*\*(.*)\*\*', line):
        text = s.groups()[0].strip()
        if any(term in text for term in search_terms):
            return text


def is_rating(line: str, rating_terms: list = config.RATING_TERMS):
    return any(term in line for term in rating_terms)


def is_blank(line: str):
    return line == ''


def fix_time(line: str):
    for m in re.finditer(r'(\d\d?)[\.:](\d\d?)', line):
        hour, minutes = m.groups()
        fixed_hour = (int(hour) + config.TIME_CORRECTION) % 24
        line = line[: m.start()] + f'{fixed_hour:0{len(hour)}d}:{minutes}' + line[m.end() :]
    return line
