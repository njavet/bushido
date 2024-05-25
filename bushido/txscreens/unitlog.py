from textual.screen import ModalScreen
from textual.widgets import Label, RichLog, Input
from textual.containers import Grid
from textual.validation import Function
from textual.app import ComposeResult
from textual.suggester import Suggester
from textual import events


class UnitLog(ModalScreen):

    BINDINGS = [('q', 'app.pop_screen', 'Back'),
                ('l', 'app.pop_screen', 'Back')]

    def __init__(self, emoji2proc, tg_client):
        super().__init__()
        self.emoji2uname = self._create_emoji2uname_dict(emoji2proc)
        self.tg_client = tg_client

    @staticmethod
    def _create_emoji2uname_dict(emoji2proc):
        dix = {}
        for emoji, proc in emoji2proc.items():
            dix[emoji] = proc.unit_name
        return dix

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Unit Log'),
            TextInput(validators=[Function(self.is_valid_key,
                                           'Not a valid key')],
                      suggester=UnitSuggester(self.emoji2uname)),
            RichLog(id='response'),
            id='unit_log')

    def is_valid_key(self, value: str) -> bool:
        try:
            return value.split()[0] in [e for e in self.emoji2uname.keys()]
        except IndexError:
            return False

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one('#response', RichLog)
        if not event.validation_result.is_valid:
            rl.clear()
            rl.write('\n'.join(event.validation_result.failure_descriptions))
        else:
            rl.clear()
            msg = await self.tg_client.send_message('csm101_bot', event.value)
            if msg:
                self.dismiss(True)
            else:
                rl.write('err')
            self.query_one(Input).action_delete_left_all()
            self.query_one(Input).action_delete_right_all()


class TextInput(Input):
    def __init__(self, validators, suggester):
        super().__init__(validators=validators,
                         suggester=suggester,
                         id='text_input')

    def on_suggestion_ready(self, event) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: events.Key) -> None:
        # workaround for accepting autocompletion
        if event.key == 'space':
            self.action_cursor_right()


class UnitSuggester(Suggester):
    def __init__(self, emoji2uname):
        super().__init__()
        self.emoji2uname = emoji2uname

    async def get_suggestion(self, value: str) -> str | None:
        es = [e for e, n in self.emoji2uname.items() if n.startswith(value)]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + '  '
