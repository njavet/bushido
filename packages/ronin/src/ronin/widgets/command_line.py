from typing import override

from rich.console import Group
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.message import Message
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Input, Static


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
            suggester=suggester,
            id="text_input",
            placeholder="enter unit...",
        )

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # Workaround for accepting autocompletion.
        if event.key == "space":
            self.action_cursor_right()
            event.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(CommandSubmitted(event.value.strip()))


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


class CommandLine(Widget):
    def __init__(self, commands: list[str]) -> None:
        super().__init__()
        self.suggester = CommandSuggester(commands)

    @override
    def compose(self) -> ComposeResult:
        with Vertical(id="log_unit_dialog"):
            yield Static(
                " BUSHIDO // CITADEL                           LOG UNIT ",
                id="terminal_header",
            )
            yield UnitHelpWidget()
            yield Static(
                "────────────────────────────────────────────────────",
                classes="separator",
            )
            yield Static("> ", id="prompt")
            yield CommandInput(suggester=self.suggester)
            yield Static(
                "SYSTEM READY // AWAITING INPUT",
                id="terminal_status",
            )


"""
    async def on_command_submitted(self, message: CommandSubmitted) -> None:
        if not message.value:
            self.notify(
                "empty domain",
                title="logging failed",
                severity="error",
            )
            return

        try:
            unit = await self.api.log_unit(line=message.value)
        except Exception as exc:
            self.notify(
                str(exc),
                title="logging failed",
                severity="error",
            )
            return

        self.notify(
            f"logged unit: {message.value.split()[0]}",
            title="logging successful",
            severity="information",
        )
"""
