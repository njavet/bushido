from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Log

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Warn
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
        self.text_log.write("Bushido TUI ready. Type commands like:")
        self.text_log.write("$ squat 100 5 180 100 5 # this is a test")
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
            self.text_log.write(f"logged {pu.name}: {pu.data}")
        elif isinstance(res, Warn):
            pu = res.value
            self.text_log.write(f"{res.message} → {pu.name}: {pu.data}")
        elif isinstance(res, Err):
            self.text_log.write(f"{res.message}")

    def handle_command(self, line: str) -> str:
        with self.sf.session() as session:
            res = log_unit(line, self.factory, session)
        return res.value
