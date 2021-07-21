import re

from portve import config


def match_search_term(text: str, search_terms: list = config.SEARCH_TERMS):
    if s := re.search(r'\*\*(.*)\*\*', text):
        text = s.groups()[0].strip()
        if any(term in text for term in search_terms):
            return text


def is_rating(text: str, rating_terms: list = config.RATING_TERMS):
    return any(term in text for term in rating_terms)


def fix_time(line: str):
    for m in re.finditer(r'(\d\d?)[\.:](\d\d?)', line):
        hour, minutes = m.groups()
        fixed_hour = (int(hour) + config.TIME_CORRECTION) % 24
        line = line[: m.start()] + f'{fixed_hour:0{len(hour)}d}:{minutes}' + line[m.end() :]
    return line


def escape_telegram_chars(text):
    # https://core.telegram.org/bots/api#formatting-options
    return text.translate(str.maketrans(config.TELEGRAM_ESCAPING_MAP))


def format_case(text):
    text = text.title()
    uppercase_map = {k.title(): k for k in config.KEEP_IN_UPPERCASE}
    for word, replacement in uppercase_map.items():
        text = text.replace(word, replacement)
    return text


def prepare_output(text):
    return format_case(escape_telegram_chars(fix_time(text)))
