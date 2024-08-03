import collections
import datetime
from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import RichLog, Static, Collapsible

import dt_functions


class UnitHistory(Static):
    def __init__(self, um):
        super().__init__()
        self.um = um

    def compose(self) -> ComposeResult:
        yield RichLog()
        with Collapsible():
            yield Static('yo')

    def get_date2msg(self):
        dix = collections.defaultdict(list)
        for umsg in self.um.retrieve_unit_messages():
            cet_dt = dt_functions.get_datetime_from_unix_timestamp(umsg.unix_timestamp)
            bushido_date = dt_functions.get_bushido_date_from_datetime(cet_dt)
            dix[bushido_date].append((umsg.umoji,
                                      umsg.message.payload,
                                      datetime.datetime.strftime(cet_dt,
                                                                 '%H:%M'))
                                     )
        return dix

    def on_mount(self):
        rl = self.query_one(RichLog)

        # TODO from a user config file
        day = datetime.date(2024, 7, 7)
        day = datetime.date(2023, 1, 1)
        date2msg = self.get_date2msg()
        while day <= datetime.date.today():
            title = datetime.date.strftime(day, '%d.%m.%y')
            lst = []
            for msg_tuple in date2msg[day]:
                if len(msg_tuple[0]) == 2:
                    e = msg_tuple[0] + '  '
                else:
                    e = msg_tuple[0] + ' '
                lst.append(msg_tuple[2] + '  ' + e + msg_tuple[1])

            text = Text('\n'.join(lst))
            rl.write(Panel(text,
                           title=title,
                           width=90,
                           title_align='left'))
            day += datetime.timedelta(days=1)

    def update_history(self):
        rl = self.query_one(RichLog)
        msg = (Message
               .select(Message, db.Unit)
               .join(db.Unit)
               .order_by(db.Unit.unix_timestamp.desc())).get()

        cet_dt = helpers.get_datetime_from_unix_timestamp(
            msg.unit.unix_timestamp
        )
        time_str = datetime.datetime.strftime(cet_dt, '%H:%M')
        if len(msg.unit.emoji) == 2:
            e = msg.unit.emoji + '  '
        else:
            e = msg.unit.emoji + ' '
        text = Text(time_str + '  ' + e + msg.payload)
        rl.write(Panel(text,
                       title='yo',
                       width=90,
                       title_align='left'))
        ld = helpers.get_bushido_date_from_datetime(cet_dt)


