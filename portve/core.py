import datetime

import html2text
import requests
import telegram

from portve import config, services


class Schedule:
    def __init__(self, channel: str, date=datetime.date.today()):
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
    def __init__(self, channels: list[str] = config.CHANNELS, date: datetime.date = None):
        self.date = (
            datetime.date.today() + datetime.timedelta(days=1) if date is None else date
        )
        self.guide = {}
        for channel in channels:
            if schedule := Schedule(channel=channel, date=self.date):
                self.guide[channel] = schedule

    def notify(self):
        bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
        bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            text=str(self),
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    def __bool__(self):
        return len(self.guide.keys()) > 0

    def __str__(self):
        buffer = []
        buffer.append(f'⚡ __Programación {self.date.strftime("%d/%m/%Y")}__\n')
        for channel, schedule in self.guide.items():
            buffer.append(f'📺 *{channel}*')
            buffer.append(str(schedule))
            buffer.append('\n')
        buffer.append(f'_ — Timezone: {services.escape_telegram_chars(config.TARGET_TZ)}_')
        buffer.append(f'_ — Fuente: [RTVE]({config.RTVE_SCHED_ROOT_URL})_')
        return '\n'.join(buffer).strip()
