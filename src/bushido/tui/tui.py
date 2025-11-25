from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Key
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Footer, Input
from textual_image.widget import Image as ImageWidget

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Warn
from bushido.modules.factory import Factory
from bushido.modules.timeline import fetch_display_units
from bushido.service.log_unit import log_unit
from bushido.tui.emojis import un2emoji
from bushido.tui.txwidgets.binary_clock import BinaryClock
from bushido.tui.txwidgets.unit_log import UnitLog


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    TITLE = "bushido"
    CSS_PATH = "main.tcss"

    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
        with self.sf.session() as session:
            units = fetch_display_units(session)
        self.unit_log = UnitLog(units, un2emoji)

    def compose(self) -> ComposeResult:
        with Horizontal(id="status_bar"):
            yield ImageWidget("src/bushido/static/belts/black_belt.png", id="belt")
            yield ImageWidget("src/bushido/static/belts/rank.png", id="rank")
            yield BinaryClock(id="clock")
        yield TextInput(suggester=UnitSuggester(un2emoji))
        yield self.unit_log
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value.strip()
        event.input.value = ""
        if not line:
            return

        with self.sf.session() as session:
            res = log_unit(line, self.factory, session)

        if isinstance(res, Ok):
            pu = res.value
            self.unit_log.write(f"logged {pu}")
        elif isinstance(res, Warn):
            self.text_log.write(f"{res.message}")
        elif isinstance(res, Err):
            self.text_log.write(f"ERROR: {res.message}")


"""
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one("#response", RichLog)
        rl.clear()
        rl.write(msg.message)
        self.query_one(Input).action_delete_left_all()
        self.query_one(Input).action_delete_right_all()
"""


class UnitSuggester(Suggester):
    def __init__(self, emojis: dict[str, str]) -> None:
        super().__init__()
        self.emojis = emojis

    async def get_suggestion(self, value: str) -> str | None:
        es = [emoji for uname, emoji in self.emojis.items() if uname.startswith(value)]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + "  "
        return None


class TextInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
