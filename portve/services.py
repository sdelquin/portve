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
