import re

import logzero

from portve import moment, settings


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
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def match_search_term(text: str, search_terms: list = settings.SEARCH_TERMS):
    if s := re.search(r'\*\*(.*)\*\*', text):
        text = s.groups()[0].strip()
        if any(term in text for term in search_terms):
            return text


def is_rating(text: str, rating_terms: list = settings.RATING_TERMS):
    return any(term in text for term in rating_terms)


def escape_telegram_chars(text):
    # https://core.telegram.org/bots/api#formatting-options
    return text.translate(str.maketrans(settings.TELEGRAM_ESCAPING_MAP))


def format_case(text):
    text = text.title()
    uppercase_map = {k.title(): k for k in settings.KEEP_IN_UPPERCASE}
    for word, replacement in uppercase_map.items():
        text = text.replace(word, replacement)
    return text


def prepare_output(text):
    return format_case(
        escape_telegram_chars(
            moment.fix_timezone(text, settings.RTVE_TZ, settings.TARGET_TZ)
        )
    )
