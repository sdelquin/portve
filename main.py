import datetime

import config
import services

guide = {}

for channel in config.CHANNELS:
    if schedule := services.get_schedule(
        channel=channel, date=datetime.date.today() + datetime.timedelta(days=3)
    ):
        guide[channel] = schedule

print(guide)
