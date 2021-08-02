import datetime
import re

import pytz


def get_utcoffset(tz: pytz.timezone):
    return datetime.datetime.now(tz=tz).utcoffset().total_seconds() / 60 / 60


def fix_timezone(line: str, source_tz: pytz.timezone, target_tz: pytz.timezone):
    delta_tz = int(get_utcoffset(target_tz) - get_utcoffset(source_tz))
    for m in re.finditer(r'(\d\d?)[\.:](\d\d?)', line):
        hour, minutes = m.groups()
        fixed_hour = (int(hour) + delta_tz) % 24
        line = line[: m.start()] + f'{fixed_hour:0{len(hour)}d}:{minutes}' + line[m.end() :]
    return line


def build_date_from_ref(ref_date: str, tz: pytz.timezone):
    today = datetime.datetime.now(tz=tz).date()
    if ref_date == 'today':
        return today
    if ref_date == 'tomorrow':
        return today + datetime.timedelta(days=1)
    return today
