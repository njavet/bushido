import collections
import datetime
from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import RichLog, Static, Collapsible
from textual.containers import ScrollableContainer
from dotenv import load_dotenv
import os

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
                 .select()
                 .where(Message.from_id == self.me.agent_id)
                 .order_by(Message.unix_timestamp)
                 )

        date2msg = collections.defaultdict(list)
        for msg in query:
            cet_dt = helpers.get_datetime_from_unix_timestamp(msg.unix_timestamp)
            ld = helpers.get_bushido_date_from_datetime(cet_dt)
            date2msg[ld].append(msg)

        day = datetime.date(2023, 1, 1)
        while day <= datetime.date.today():
            title = datetime.date.strftime(day, '%d.%m.%y')
            lst = []
            for msg in date2msg[day]:
                cet_dt = helpers.get_datetime_from_unix_timestamp(msg.unix_timestamp)
                time_str = datetime.datetime.strftime(cet_dt, '%H:%M')
                lst.append(msg.emoji_payload + ' ' + time_str)
            text = Text('\n'.join(lst), justify='right')
            rl.write(Panel(text,
                           title=title,
                           width=90,
                           title_align='left'))
            day += datetime.timedelta(days=1)



