from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Input
from textual_image.widget import Image as ImageWidget

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Result, Warn
from bushido.modules.factory import Factory
from bushido.service.log_unit import log_unit
from bushido.tui.txwidgets.binary_clock import BinaryClock
from bushido.tui.txwidgets.terminal import Terminal


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
        self.terminal = Terminal(session_factory, factory)

    def compose(self) -> ComposeResult:
        with Horizontal(id="status_bar"):
            yield ImageWidget("src/bushido/static/belts/black_belt.png", id="belt")
            yield ImageWidget("src/bushido/static/belts/rank.png", id="rank")
            yield BinaryClock(id="clock")
        yield self.terminal
        yield Footer()

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
