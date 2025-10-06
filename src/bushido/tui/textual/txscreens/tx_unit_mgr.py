from textual import events
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.suggester import Suggester
from textual.widgets import Input, Label, RichLog


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
