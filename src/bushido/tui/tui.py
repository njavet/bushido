from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Static, TextLog

from bushido.modules.db import get_session  # your contextmanager
from bushido.modules.dtypes import Err, Ok, Result, UnitData, Warn
from bushido.modules.factory import Factory


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("h", "help", "Help"),
        ("m", "manage_units", "Unit"),
    ]
    CSS_PATH = None
    TITLE = "Bushido"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Bushido TUI is running. Press Q to quit.")
        yield Footer()


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    TITLE = "Bushido"

    def __init__(self, factory: Factory) -> None:
        super().__init__()
        self.factory = factory
        self.log: TextLog
        self.input: Input

    def compose(self) -> ComposeResult:
        yield Header()
        self.log = TextLog(highlight=False, markup=False)
        self.log.write("Bushido TUI ready. Type commands like:")
        self.log.write("$ squat 100 5 180 100 5 # this is a test")
        yield self.log
        self.input = Input(placeholder="$ ")
        yield self.input
        yield Footer()

    async def on_mount(self) -> None:
        await self.input.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value.strip()
        event.input.value = ""
        if not line:
            return

        # echo the command
        self.log.write(f"$ {line}")

        # process
        res = self.handle_command(line)

        # display result
        if isinstance(res, Ok):
            pu = res.value
            self.log.write(f"✔ logged {pu.name}: {pu.data}", style="green")
        elif isinstance(res, Warn):
            pu = res.value
            self.log.write(f"⚠ {res.message} → {pu.name}: {pu.data}", style="yellow")
        elif isinstance(res, Err):
            self.log.write(f"✖ {res.message}", style="red")

    def handle_command(self, line: str) -> Result[UnitData]:
        # very simple: first token = unit_name, rest = data
        parts = line.split(maxsplit=1)
        unit_name = parts[0]
        payload = parts[1] if len(parts) > 1 else ""

        parser = self.factory.parsers.get(unit_name)
        if parser is None:
            return Err(message=f"Unknown unit: {unit_name}")

        parsed = parser.parse(payload)
        if isinstance(parsed, Err):
            return parsed

        # persist to DB
        from bushido.modules.repo import make_unit_repo_for  # whatever you have

        with get_session() as session:
            repo = make_unit_repo_for(session, parsed.value.name)  # map name → UnitRepo
            orm_unit, sub_rows = self.factory.mappers[unit_name].to_orm(parsed.value)
            repo.add_unit(orm_unit, sub_rows)

        return parsed
