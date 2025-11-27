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
        self.emojis = emojis
        self.scroll_container = ScrollableContainer()
        self.bdate2units = self.get_bdate2units(units)
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
        self,
        units: list[DisplayUnit],
    ) -> dict[datetime.date, list[str]]:
        dix: dict[datetime.date, list[str]] = collections.defaultdict(list)
        for d in units:
            bd = get_bushido_date_from_datetime(d.log_time)
            dix[bd].append(self.create_display_str(d))
        return dix

    def create_display_str(self, unit: DisplayUnit) -> str:
        if unit.payload:
            res = self.emojis[unit.name] + " " + unit.payload
        else:
            res = self.emojis[unit.name]
        return res

    def update_view(self, unit: DisplayUnit) -> None:
        display_str = self.create_display_str(unit)
        day = get_bushido_date_from_datetime(unit.log_time)
        self.bdate2units[day].insert(0, display_str)
        print("before", self.bdate2units[day])
        try:
            dw = self.bdate2dw[day]
            text = "\n".join(self.bdate2units[day])
            print("text", text)
            dw.content = text
        except KeyError:
            dw = self.create_day_widget(day)
            self.scroll_container.mount(dw)
