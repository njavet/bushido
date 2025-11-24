from textual import events
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.suggester import Suggester
from textual.widgets import Footer, Header, Input, Label, Log, RichLog

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Result, Warn
from bushido.modules.factory import Factory
from bushido.service.log_unit import log_unit
from bushido.tui.emojis import emojis


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    TITLE = "Bushido"

    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
        self.text_log = Log(highlight=False)
        self.input = Input(placeholder="$ ")

    def compose(self) -> ComposeResult:
        yield Header()
        self.text_log.write("Bushido TUI ready. Type commands like\n:")
        yield self.text_log
        yield self.input
        yield Grid(
            Label("Unit Log"),
            TextInput(suggester=UnitSuggester(emojis)),
            RichLog(id="response"),
            id="unit_log",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.input.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value.strip()
        event.input.value = ""
        if not line:
            return

        # echo the command
        self.text_log.write(f"$ {line}")

        # process
        res = self.handle_command(line)

        # display result
        if isinstance(res, Ok):
            pu = res.value
            self.text_log.write(f"logged {pu}")
        elif isinstance(res, Warn):
            self.text_log.write(f"{res.message}")
        elif isinstance(res, Err):
            self.text_log.write(f"ERROR: {res.message}")

    def handle_command(self, line: str) -> Result[str]:
        with self.sf.session() as session:
            res = log_unit(line, self.factory, session)
        return res


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
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: events.Event) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: events.Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
