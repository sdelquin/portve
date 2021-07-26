from pathlib import Path

import pytz
from prettyconf import config

PROJECT_DIR = Path(__file__).absolute().parent.parent

RATING_TERMS = config(
    'RATING_TERMS',
    default='NO RECOMENDADO, SIN CALIFICAR, PARA TODOS LOS PUBLICOS',
    cast=config.list,
)
SEARCH_TERMS = config('SEARCH_TERMS', cast=config.list)

CHANNELS = config('CHANNELS', default='LA1, LA2, TELEDEPORTE, 24H, CLAN', cast=config.list)

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = config('TELEGRAM_CHANNEL_ID')

RTVE_SCHED_URL = config(
    'RTVE_SCHED_URL',
    default='https://www.rtve.es/'
    'contenidos/sala-de-comunicacion/programacion-descargable/'
    '{channel}_{date}.html',
)
RTVE_SCHED_ROOT_URL = config(
    'RTVE_SCHED_ROOT_URL', default='https://www.rtve.es/television/programacion/'
)

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
RTVE_TZ = config('RTVE_TZ', default='Europe/Madrid', cast=lambda tz: pytz.timezone(tz))
TARGET_TZ = config('TARGET_TZ', default='UTC', cast=lambda tz: pytz.timezone(tz))

TELEGRAM_ESCAPING_MAP = {
    '_': r'\_',
    '*': r'\*',
    '[': r'\[',
    ']': r'\]',
    '(': r'\(',
    ')': r'\)',
    '~': r'\~',
    '`': r'\`',
    '>': r'\>',
    '#': r'\#',
    '+': r'\+',
    '-': r'\-',
    '=': r'\=',
    '|': r'\|',
    '{': r'\{',
    '}': r'\}',
    '.': r'\.',
    '!': r'\!',
}

KEEP_IN_UPPERCASE = config('KEEP_IN_UPPERCASE', default='', cast=config.list)

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_DIR.name + '.log'))
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

REDIS_DB = config('REDIS_DB', default=0, cast=int)
