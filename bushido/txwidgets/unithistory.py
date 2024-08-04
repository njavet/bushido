import collections
from dataclasses import dataclass
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
        self.bdate_to_umsg = self.get_date2msg()
        self.bdate_to_panels = {}

    def compose(self) -> ComposeResult:
        yield RichLog()
        with Collapsible():
            yield Static('yo')

    def on_mount(self):
        rl = self.query_one(RichLog)
        # TODO from a user config file
        day = datetime.date(2024, 7, 14)

        while day <= datetime.date.today():
            panel = self.create_panel(day)
            rl.write(panel)
            day += datetime.timedelta(days=1)

    @dataclass
    class UnitMessage:
        text: str
        comment: str | None
        bushido_date: datetime.date

    def create_unit_message(self, umsg):
        cet_dt = dt_functions.get_datetime_from_unix_timestamp(
            umsg.unit.unix_timestamp
        )
        bushido_date = dt_functions.get_bushido_date_from_datetime(cet_dt)
        local_time = datetime.datetime.strftime(cet_dt, '%H:%M')
        if len(umsg.unit.umoji) == 2:
            text = ' '.join([local_time, umsg.unit.umoji + ' ', umsg.payload])
        else:
            text = ' '.join([local_time, umsg.unit.umoji, umsg.payload])

        return self.UnitMessage(text=text,
                                comment=umsg.comment,
                                bushido_date=bushido_date)

    def create_panel(self, day):
        title = datetime.date.strftime(day, '%d.%m.%y')
        text = Text('\n'.join(self.bdate_to_umsg[day]))
        panel = Panel(text, title=title, width=90, title_align='left')
        self.bdate_to_panels[day] = panel
        return panel

    def get_date2msg(self):
        dix = collections.defaultdict(list)
        for umsg in self.um.retrieve_unit_messages():
            unit_message = self.create_unit_message(umsg)
            dix[unit_message.bushido_date].append(unit_message.text)
        return dix

    def update_view(self, sender):
        unit_message = self.create_unit_message(sender)
        day = unit_message.bushido_date
        self.bdate_to_umsg[day].append(unit_message.text)
        panel = self.create_panel(day)
        rl = self.query_one(RichLog)
        rl.write(panel)
