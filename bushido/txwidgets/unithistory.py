import collections
import datetime
from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import RichLog, Static

import db
from db import Message
import helpers


class UnitHistory(Static):
    def __init__(self):
        super().__init__()
        self.me = db.get_me()

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_mount(self):
        rl = self.query_one(RichLog)
        query = (Message
                 .select(Message, db.Unit)
                 .join(db.Unit)
                 .order_by(db.Unit.unix_timestamp))

        date2msg = collections.defaultdict(list)
        for msg in query:
            cet_dt = helpers.get_datetime_from_unix_timestamp(
                msg.unit.unix_timestamp
            )
            ld = helpers.get_bushido_date_from_datetime(cet_dt)
            date2msg[ld].append(msg)

        # TODO from a user config file
        day = datetime.date(2024, 5, 26)
        day = datetime.date(2023, 1, 1)
        while day <= datetime.date.today():
            title = datetime.date.strftime(day, '%d.%m.%y')
            lst = []
            for msg in date2msg[day]:
                cet_dt = helpers.get_datetime_from_unix_timestamp(
                    msg.unit.unix_timestamp
                )
                time_str = datetime.datetime.strftime(cet_dt, '%H:%M')
                if len(msg.unit.emoji) == 2:
                    e = msg.unit.emoji + '  '
                else:
                    e = msg.unit.emoji + ' '
                lst.append(time_str + '  ' + e + msg.payload)

            text = Text('\n'.join(lst))
            rl.write(Panel(text,
                           title=title,
                           width=90,
                           title_align='left'))
            day += datetime.timedelta(days=1)



