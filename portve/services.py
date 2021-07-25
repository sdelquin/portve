import datetime
import re

import logzero

from portve import config


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        config.LOGFILE,
        maxBytes=config.LOGFILE_SIZE,
        backupCount=config.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def get_timezone_offset(value):
    value = value.strip().upper()
    if m := re.match(r'UTC(?:\s*([+-]?\s*\d+))?', value):
        offset = m.groups()[0]
        if offset is not None:
            return eval(offset)
    return 0


DELTA_TZ = get_timezone_offset(config.TARGET_TZ) - get_timezone_offset(config.RTVE_TZ)


def match_search_term(text: str, search_terms: list = config.SEARCH_TERMS):
    if s := re.search(r'\*\*(.*)\*\*', text):
        text = s.groups()[0].strip()
        if any(term in text for term in search_terms):
            return text


def is_rating(text: str, rating_terms: list = config.RATING_TERMS):
    return any(term in text for term in rating_terms)


def fix_timezone(line: str, delta_tz=DELTA_TZ):
    for m in re.finditer(r'(\d\d?)[\.:](\d\d?)', line):
        hour, minutes = m.groups()
        fixed_hour = (int(hour) + delta_tz) % 24
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
    return format_case(escape_telegram_chars(fix_timezone(text)))


def build_ref_date(ref_date: str):
    if ref_date == 'today':
        return datetime.date.today()
    if ref_date == 'tomorrow':
        return datetime.date.today() + datetime.timedelta(days=1)
    return datetime.date.today()
