from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Log

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Result, UnitData, Warn
from bushido.modules.factory import Factory


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    TITLE = "Bushido"

    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
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

        parser_res = self.factory.get_parser(unit_name)
        if isinstance(parser_res, Err):
            return parser_res

        parser = parser_res.value
        parsed = parser.parse(payload)
        if isinstance(parsed, Err):
            return parsed

        with self.sf.session() as session:
            repo_res = self.factory.get_repo(unit_name, session)
            if isinstance(repo_res, Err):
                return repo_res
            repo = repo_res.value
            mapper_res = self.factory.get_mapper(unit_name)
            if isinstance(mapper_res, Err):
                return mapper_res
            mapper = mapper_res.value
            orm_unit, sub_rows = mapper.to_orm(parsed.value)
            repo.add_unit(orm_unit, sub_rows)

        return parsed
