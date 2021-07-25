import datetime

import html2text
import redis
import requests
import telegram
from logzero import logger

from portve import config, services


class Schedule:
    def __init__(self, channel: str, date=datetime.date.today()):
        logger.info(f'Building schedule for {channel} at {date}')
        self.url = config.RTVE_SCHED_URL.format(
            channel=channel, date=date.strftime('%d%m%Y')
        )
        response = requests.get(self.url)
        self.page = html2text.html2text(response.text)
        self.schedule = self._get_schedule()

    def _get_schedule(self):
        schedule = {}
        add_details = False

        for line in self.page.split('\n'):
            line = line.strip()
            if not add_details and (heading := services.match_search_term(line)):
                schedule[heading] = []
                add_details = True
                continue
            if services.is_rating(line):
                add_details = False
                continue
            if add_details and line != '':
                schedule[heading].append(line)

        return schedule

    def __bool__(self):
        return len(self.schedule.keys()) > 0

    def __str__(self):
        buffer = []
        for heading, details in self.schedule.items():
            buffer.append(f'• {services.prepare_output(heading)}')
            if details:
                buffer.append(
                    '\n'.join(
                        [
                            f'\t\t\t\t_{services.prepare_output(detail)}_'
                            for detail in details
                        ]
                    )
                )
        return '\n'.join(buffer)


class TVGuide:
    def __init__(
        self,
        channels: list[str] = config.CHANNELS,
        date: datetime.date = datetime.date.today(),
    ):
        logger.debug('Building TVGuide object')
        self.redis = redis.Redis(db=config.REDIS_DB)
        self.date = date
        self.tg_bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
        self.guide = {}
        for channel in channels:
            if schedule := Schedule(channel=channel, date=self.date):
                self.guide[channel] = schedule
        logger.debug(self)

    def send_guide(self):
        return self.tg_bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            text=str(self),
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    def edit_guide(self, msg_id: str):
        return self.tg_bot.edit_message_text(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            message_id=msg_id,
            text=str(self),
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    def notify(self):
        logger.info('Notifying guide to Telegram channel')
        try:
            if msg_id := self.redis.get(self.date.isoformat()):
                self.edit_guide(msg_id.decode('utf-8'))
            else:
                msg = self.send_guide()
                self.redis.set(self.date.isoformat(), msg.message_id)
        except telegram.error.BadRequest as err:
            logger.error(err)

    def __bool__(self):
        return len(self.guide.keys()) > 0

    def __str__(self):
        buffer = []
        buffer.append(f'⚡ __Programación {self.date.strftime("%d/%m/%Y")}__\n')
        for channel, schedule in self.guide.items():
            buffer.append(f'📺 *{channel}*')
            buffer.append(str(schedule) + '\n')
        else:
            buffer.append('No hay información disponible\n')
        buffer.append(f'_ — Timezone: {services.escape_telegram_chars(config.TARGET_TZ)}_')
        buffer.append(f'_ — Fuente: [RTVE]({config.RTVE_SCHED_ROOT_URL})_')
        return '\n'.join(buffer).strip()
