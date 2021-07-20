import datetime
import re
from typing import DefaultDict

import html2text
import requests
import telegram

import config


def match_search_term(line: str):
    if s := re.search(r'\*\*(.*)\*\*', line):
        text = s.groups()[0].strip()
        if any(term in text for term in config.SEARCH_TERMS):
            return text


def is_rating(line: str):
    return any(term in line for term in config.RATING_TERMS)


def is_blank(line: str):
    return line == ''


def get_schedule(channel: str, date: datetime.date = datetime.date.today()):
    url = config.RTVE_SCHED_URL.format(channel=channel, date=date.strftime('%d%m%Y'))
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

    return schedule


def send_guide(guide: dict):
    bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
    bot.send_message(
        chat_id=config.TELEGRAM_CHANNEL_ID,
        text='just testing',
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )
