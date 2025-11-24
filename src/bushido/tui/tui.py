from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Log

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Result, UnitData, Warn


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    TITLE = "Bushido"

    def __init__(self, session_factory: SessionFactory) -> None:
        super().__init__()
        self.sf = SessionFactory
        self.text_log: Log | None = None
        self.input: Input | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.text_log = Log(highlight=False)
        self.text_log.write("Bushido TUI ready. Type commands like:")
        self.text_log.write("$ squat 100 5 180 100 5 # this is a test")
        yield self.text_log
        self.input = Input(placeholder="$ ")
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
