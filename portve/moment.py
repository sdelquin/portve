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


def build_ref_date(ref_date: str):
    if ref_date == 'today':
        return datetime.date.today()
    if ref_date == 'tomorrow':
        return datetime.date.today() + datetime.timedelta(days=1)
    return datetime.date.today()
