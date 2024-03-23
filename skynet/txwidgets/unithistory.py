import collections
import datetime

from rich.panel import Panel
from textual.app import ComposeResult
from textual.widgets import RichLog, Static, Collapsible
from textual.containers import ScrollableContainer

from db import Message
from txwidgets import styles
from utils import utilities


class UnitHistory(Static):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_mount(self):
        rl = self.query_one(RichLog)
        query = (Message
                 .select()
                 .where(Message.user_id == self.user_id)
                 .order_by(Message.log_time)
                 )

        date2msg = collections.defaultdict(list)
        for msg in query:
            ld = utilities.get_date_from_logtime(msg.log_time)
            date2msg[ld].append(msg)

        day = datetime.date(2023, 1, 1)
        while day <= datetime.date.today():
            title = datetime.date.strftime(day, '%d.%m.%y')
            lst = []
            for msg in date2msg[day]:
                time_str = datetime.datetime.strftime(msg.log_time, '%H:%M:%S')
                lst.append(time_str + ' ' + msg.msg)
            rl.write(Panel('\n'.join(lst),
                           title=title,
                           width=90,
                           title_align='left'))
            day += datetime.timedelta(days=1)



