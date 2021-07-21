from prettyconf import config

RATING_TERMS = config(
    'RATING_TERMS',
    default='NO RECOMENDADO, SIN CALIFICAR, PARA TODOS LOS PUBLICOS',
    cast=config.list,
)
SEARCH_TERMS = config('SEARCH_TERMS', cast=config.list)

CHANNELS = config('CHANNELS', default='LA1, LA2, TELEDEPORTE', cast=config.list)

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

TIME_CORRECTION = config('TIME_CORRECTION', default=0, cast=int)
