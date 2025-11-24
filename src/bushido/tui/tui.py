from textual import events
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.suggester import Suggester
from textual.widgets import Footer, Header, Input, Label, Log, RichLog

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Result, Warn
from bushido.modules.factory import Factory
from bushido.service.log_unit import log_unit


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


class TxUnitManager(ModalScreen):
    BINDINGS = [("q", "app.pop_screen", "Back"), ("m", "app.pop_screen", "Back")]

    def __init__(self, um, tg_agent):
        super().__init__()
        self.um = um
        self.tg_agent = tg_agent

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Unit Log"),
            TextInput(suggester=UnitSuggester(self.um)),
            RichLog(id="response"),
            id="unit_log",
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one("#response", RichLog)
        rl.clear()
        msg = await self.tg_agent.send_message("csm101_bot", event.value)
        rl.write(msg.message)
        self.query_one(Input).action_delete_left_all()
        self.query_one(Input).action_delete_right_all()


class TextInput(Input):
    def __init__(self, suggester):
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: events.Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()


class UnitSuggester(Suggester):
    def __init__(self, um):
        super().__init__()
        self.um = um
        self.uname2umoji = self.construct_dict()

    def construct_dict(self):
        dix = {}
        for umoji, proc in self.um.umoji2proc.items():
            dix[proc.uname] = umoji
        return dix

    async def get_suggestion(self, value: str) -> str | None:
        es = [
            umoji
            for uname, umoji in self.uname2umoji.items()
            if uname.startswith(value)
        ]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + "  "
