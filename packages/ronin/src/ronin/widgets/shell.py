from typing import override

from rich.console import Group
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.message import Message
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Input, Static


class Shell(Container):
    def __init__(self, commands: list[str]) -> None:
        super().__init__()
        self.commands = commands

    @override
    def compose(self) -> ComposeResult:
        yield CommandLine(commands=self.commands)
        yield ShellView()


class ShellView(Container):
    @override
    def compose(self) -> ComposeResult:
        yield Static("YOO")

    async def show(self, widget: Widget) -> None:
        await self.remove_children()
        await self.mount(widget)


class CommandLine(Widget):
    def __init__(self, commands: list[str]) -> None:
        super().__init__()
        self.suggester = CommandSuggester(commands)

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="command_line"):
            yield Static(" >_", id="prompt")
            yield CommandInput(suggester=self.suggester)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(CommandSubmitted(event.value.strip()))


class CommandSuggester(Suggester):
    def __init__(self, commands: list[str]) -> None:
        super().__init__()
        self.commands = commands

    @override
    async def get_suggestion(self, value: str) -> str | None:
        names = [name for name in self.commands if name.startswith(value)]
        if len(names) == 1:
            return names[0] + " "
        return None


class CommandInput(Input):
    def __init__(self, suggester: CommandSuggester) -> None:
        super().__init__(
            suggester=suggester, id="command_input", placeholder="enter command..."
        )

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # Workaround for accepting autocompletion.
        if event.key == "space":
            self.action_cursor_right()
            event.stop()


class CommandSubmitted(Message):
    def __init__(self, line: str) -> None:
        super().__init__()
        self.line = line


class UnitHelpWidget(Widget):
    @override
    def render(self) -> Group:
        header = Text()
        header.append("CITADEL ", style="bold #72f3ff")
        header.append("// UNIT LOGGER", style="#608890")

        grammar = Text()
        grammar.append("grammar  ", style="#608890")
        grammar.append("<unit> <arguments> [--options]", style="#b8dce2")

        hint = Text()
        hint.append("tab/space ", style="#45e6f2")
        hint.append("autocomplete    ", style="#608890")
        hint.append("enter ", style="#45e6f2")
        hint.append("submit    ", style="#608890")
        hint.append("esc ", style="#45e6f2")
        hint.append("abort", style="#608890")

        return Group(
            header,
            "",
            grammar,
            hint,
        )
