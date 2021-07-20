from prettyconf import config

RTVE_SCHED_URL = config(
    'RTVE_SCHED_URL',
    default='https://www.rtve.es/'
    'contenidos/sala-de-comunicacion/programacion-descargable/'
    '{channel}_{date}.html',
)

SEARCH_TERMS = config('SEARCH_TERMS', cast=config.list)
RATING_TERMS = config('RATING_TERMS', cast=config.list)
