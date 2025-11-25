import collections
import datetime

from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import Reactive
from textual.widgets import Static

from bushido.modules.dtypes import DisplayUnit
from bushido.parsing.utils import get_bushido_date_from_datetime


class DayWidget(Static):
    content: Reactive[str] = Reactive("")

    def __init__(self, text: str, title: str) -> None:
        super().__init__()
        self.content = text
        self.title = title

    def render(self) -> Panel:
        return Panel(Text(self.content), title=self.title, width=90, title_align="left")


class UnitLog(Static):
    def __init__(self, units: list[DisplayUnit], emojis: dict[str, str]) -> None:
        super().__init__()
        self.scroll_container = ScrollableContainer()
        self.bdate2units = self.get_bdate2units(units, emojis)
        self.bdate2dw: dict[datetime.date, DayWidget] = {}

    def compose(self) -> ComposeResult:
        yield self.scroll_container

    async def on_mount(self) -> None:
        # TODO from a user config file
        end = datetime.date(2025, 10, 12)
        day = datetime.date.today()

        while end <= day:
            dw = self.create_day_widget(day)
            await self.scroll_container.mount(dw)
            day -= datetime.timedelta(days=1)

    def create_day_widget(self, day: datetime.date) -> DayWidget:
        title = datetime.date.strftime(day, "%d.%m.%y")
        text = "\n".join(self.bdate2units[day])
        dw = DayWidget(text, title)
        self.bdate2dw[day] = dw
        return dw

    def get_bdate2units(
        self, units: list[DisplayUnit], emojis: dict[str, str]
    ) -> dict[datetime.date, list[str]]:
        dix: dict[datetime.date, list[str]] = collections.defaultdict(list)
        for d in units:
            bd = get_bushido_date_from_datetime(d.log_time)
            if d.payload:
                dix[bd].append(emojis[d.name] + " " + d.payload)
            else:
                dix[bd].append(emojis[d.name])
        return dix


"""
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

"""
