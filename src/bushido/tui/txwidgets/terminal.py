import collections
import datetime

from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.events import Key
from textual.reactive import Reactive
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Input, Static

from bushido.infra.db import SessionFactory
from bushido.modules.factory import Factory
from bushido.modules.timeline import fetch_display_units
from bushido.parsing.utils import get_bushido_date_from_datetime
from bushido.tui.emojis import emojis


class DayWidget(Static):
    content: Reactive[str] = Reactive("")

    def __init__(self, text: str, title: str) -> None:
        super().__init__()
        self.content = text
        self.title = title

    def render(self) -> Panel:
        return Panel(Text(self.content), title=self.title, width=90, title_align="left")


class Terminal(Static):
    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
        self.scroll_container = ScrollableContainer()
        self.bdate2umsg = self.get_bdate2umsg()
        self.bdate2dw: dict[datetime.date, DayWidget] = {}

    def compose(self) -> ComposeResult:
        yield self.scroll_container

    async def on_mount(self) -> None:
        # TODO from a user config file
        day = datetime.date(2025, 10, 12)
        ti = TextInput(placeholder="$", suggester=UnitSuggester(emojis))
        await self.scroll_container.mount(ti)

        while day <= datetime.date.today():
            dw = self.create_day_widget(day)
            await self.scroll_container.mount(dw)
            day += datetime.timedelta(days=1)

    def create_day_widget(self, day: datetime.date) -> DayWidget:
        title = datetime.date.strftime(day, "%d.%m.%y")
        text = "\n".join(self.bdate2umsg[day])
        dw = DayWidget(text, title)
        self.bdate2dw[day] = dw
        return dw

    def get_bdate2umsg(self) -> dict[datetime.date, list[str]]:
        dix: dict[datetime.date, list[str]] = collections.defaultdict(list)
        with self.sf.session() as session:
            dunits = fetch_display_units(session)
            for d in dunits:
                bd = get_bushido_date_from_datetime(d.log_time)
                if d.payload:
                    dix[bd].append(d.payload)
                else:
                    dix[bd].append("")
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


class UnitSuggester(Suggester):
    def __init__(self, emojis: dict[str, str]) -> None:
        super().__init__()
        self.emojis = emojis
        self.un2emoji = self.construct_dict()

    def construct_dict(self) -> dict[str, str]:
        dix: dict[str, str] = {}
        for e, n in self.emojis.items():
            dix[n] = e
        return dix

    async def get_suggestion(self, value: str) -> str | None:
        es = [
            umoji for uname, umoji in self.un2emoji.items() if uname.startswith(value)
        ]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + "  "
        return None


class TextInput(Input):
    def __init__(self, placeholder: str, suggester: UnitSuggester) -> None:
        super().__init__(placeholder=placeholder, suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
