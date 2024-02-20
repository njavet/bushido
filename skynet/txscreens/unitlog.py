# general import*s
from textual.screen import ModalScreen
from textual.validation import Function, Validator, ValidationResult
from textual.app import ComposeResult
from textual.containers import *
from textual.widgets import *
from textual.suggester import SuggestFromList, Suggester
from textual import on, events


class UnitLog(ModalScreen):

    BINDINGS = [('b', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, string_processor):
        super().__init__()
        self.user_id = user_id
        self.string_processor = string_processor

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Unit Log'),
            TextInput(validators=[Function(self.is_valid_key, 'Not a valid key')],
                      suggester=UnitSuggester(self.string_processor.emojis)),
            RichLog(id='response'),
            id='unit_log')

    def is_valid_key(self, value: str) -> bool:
        try:
            return value.split()[0] in [e for e in self.string_processor.emojis.keys()]
        except IndexError:
            return False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one('#response', RichLog)
        if not event.validation_result.is_valid:
            rl.clear()
            rl.write('\n'.join(event.validation_result.failure_descriptions))
        else:
            rl.clear()
            res = self.string_processor.process_string(event.value,
                                                       user_id=self.user_id)

            if res.success:
                rl.write('Unit confirmed!')
            else:
                rl.write(res.error)
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
    def __init__(self, emojis):
        super().__init__()
        self.emojis = emojis

    async def get_suggestion(self, value: str) -> str | None:
        dix = {}
        for e, n in self.emojis.items():
            lst = n.split('.')
            if len(lst) == 2:
                dix[e] = lst[1]
            else:
                dix[e] = lst[0]

        es = [e for e, n in dix.items() if n.startswith(value)]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + '  '


