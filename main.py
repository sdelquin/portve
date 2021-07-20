import datetime

import services

schedule = services.get_schedule(
    channel='LA1', date=datetime.date.today() + datetime.timedelta(days=3)
)
print(schedule)
