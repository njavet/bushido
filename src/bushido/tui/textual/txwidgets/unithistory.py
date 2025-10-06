import collections
import datetime
from dataclasses import dataclass

from bushido.dt_functions import (
    get_bushido_date_from_datetime,
    get_datetime_from_unix_timestamp,
)
from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import Reactive
from textual.widgets import Static


class DayWidget(Static):
    content: Reactive[str] = Reactive("")

    def __init__(self, text, title):
        super().__init__()
        self.content = text
        self.title = title

    def render(self) -> Panel:
        return Panel(Text(self.content), title=self.title, width=90, title_align="left")


class UnitHistory(Static):
    def __init__(self, um):
        super().__init__()
        self.um = um
        self.scroll_container = ScrollableContainer()
        self.bdate2umsg = self.get_bdate2umsg()
        self.bdate2dw = {}

    def compose(self) -> ComposeResult:
        yield self.scroll_container

    async def on_mount(self):
        # TODO from a user config file
        day = datetime.date(2024, 7, 14)

        while day <= datetime.date.today():
            dw = self.create_day_widget(day)
            await self.scroll_container.mount(dw)
            day += datetime.timedelta(days=1)

    @dataclass
    class UnitMessage:
        text: str
        comment: str | None
        bushido_date: datetime.date

    def create_unit_message(self, umsg):
        cet_dt = get_datetime_from_unix_timestamp(umsg.unit.unix_timestamp)
        bushido_date = get_bushido_date_from_datetime(cet_dt)
        local_time = datetime.datetime.strftime(cet_dt, "%H:%M")
        if len(umsg.unit.umoji) == 2:
            text = " ".join([local_time, umsg.unit.umoji + " ", umsg.payload])
        else:
            text = " ".join([local_time, umsg.unit.umoji, umsg.payload])

        return self.UnitMessage(
            text=text, comment=umsg.comment, bushido_date=bushido_date
        )

    def create_day_widget(self, day) -> DayWidget:
        title = datetime.date.strftime(day, "%d.%m.%y")
        text = "\n".join(self.bdate2umsg[day])
        dw = DayWidget(text, title)
        self.bdate2dw[day] = dw
        return dw

    def get_bdate2umsg(self):
        dix = collections.defaultdict(list)
        for umsg in self.um.retrieve_unit_messages():
            unit_message = self.create_unit_message(umsg)
            dix[unit_message.bushido_date].append(unit_message.text)
        return dix

    def update_view(self, sender):
        unit_message = self.create_unit_message(sender)
        day = unit_message.bushido_date
        self.bdate2umsg[day].append(unit_message.text)
        try:
            dw = self.bdate2dw[day]
            text = "\n".join(self.bdate2umsg[day])
            dw.content = text
        except KeyError:
            dw = self.create_day_widget(day)
            self.scroll_container.mount(dw)
