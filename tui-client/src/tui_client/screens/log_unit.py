import datetime
from typing import ClassVar, override

from rich.console import Group
from rich.panel import Panel
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.events import Key
from textual.message import Message
from textual.screen import ModalScreen
from textual.suggester import Suggester, SuggestionReady
from textual.widget import Widget
from textual.widgets import Input

from bushidolib.constants import UnitCategory
from bushidolib.contracts.log_req import (
    CardioLogUnitRequest,
    GymLogUnitRequest,
    LiftingLogUnitRequest,
    WimhofLogUnitRequest,
)
from bushidolib.domain.parsing import parse_raw_unit, split_options
from bushidolib.exceptions import ParsingUnitError
from tui_client.api_client import BushidoApiClient
from tui_client.settings import LOCAL_TIMEZONE


class UnitSuggester(Suggester):
    def __init__(self) -> None:
        super().__init__()
        self.unit_names: list[str] = []

    def set_unit_names(self, unit_names: list[str]) -> None:
        self.unit_names = unit_names

    @override
    async def get_suggestion(self, value: str) -> str | None:
        names = [name for name in self.unit_names if name.startswith(value)]
        if len(names) == 1:
            return names[0] + " "
        return None


class UnitInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
            event.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(UnitSubmitted(event.value.strip()))


class UnitSubmitted(Message):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class UnitHelpWidget(Widget):
    @override
    def render(self) -> Group:
        panels = []
        for item in ["yo"]:
            content = "\n".join(
                [
                    f"Grammar: {item}",
                ]
            )
            panel = Panel(
                content,
            )
            panels.append(panel)
        return Group(*panels)


class LogUnitScreen(ModalScreen[bool]):
    BINDINGS: ClassVar = [
        Binding("escape", "cancel", "cancel"),
    ]

    def __init__(self, api: BushidoApiClient) -> None:
        super().__init__()
        self.api = api
        self.unit_settings: dict[str, UnitCategory] = {}
        self.unit_suggester = UnitSuggester()

    async def action_cancel(self) -> None:
        await self.dismiss(False)

    @override
    def compose(self) -> ComposeResult:
        with Vertical(id="log_unit_dialog"):
            yield UnitHelpWidget()
            yield UnitInput(suggester=self.unit_suggester)

    async def on_mount(self) -> None:
        self.unit_settings = await self.api.load_unit_settings()
        self.unit_suggester.set_unit_names(list(self.unit_settings.keys()))

    async def on_unit_submitted(self, message: UnitSubmitted) -> None:
        if not message.value:
            self.app.notify("empty domain", title="logging failed", severity="error")
            await self.dismiss(False)
        else:
            raw_unit = parse_raw_unit(message.value)
            tokens, log_time = split_options(raw_unit.tokens, LOCAL_TIMEZONE)
            if log_time is None:
                log_time = datetime.datetime.now(LOCAL_TIMEZONE)
            try:
                unit_category = self.unit_settings[raw_unit.name]
            except KeyError as e:
                raise ParsingUnitError(f"unknown unit: {raw_unit.name}") from e

            match unit_category:
                case UnitCategory.CARDIO:
                    await self.api.log_unit(
                        CardioLogUnitRequest(
                            unit_category=unit_category,
                            unit_name=raw_unit.name,
                            tokens=tokens,
                            log_time=log_time,
                            comment=raw_unit.comment,
                        )
                    )
                case UnitCategory.GYM:
                    await self.api.log_unit(
                        GymLogUnitRequest(
                            unit_category=unit_category,
                            unit_name=raw_unit.name,
                            tokens=tokens,
                            log_time=log_time,
                            comment=raw_unit.comment,
                        )
                    )
                case UnitCategory.LIFTING:
                    await self.api.log_unit(
                        LiftingLogUnitRequest(
                            unit_category=unit_category,
                            unit_name=raw_unit.name,
                            tokens=tokens,
                            log_time=log_time,
                            comment=raw_unit.comment,
                        )
                    )
                case UnitCategory.WIMHOF:
                    await self.api.log_unit(
                        WimhofLogUnitRequest(
                            unit_category=unit_category,
                            unit_name=raw_unit.name,
                            tokens=tokens,
                            log_time=log_time,
                            comment=raw_unit.comment,
                        )
                    )
            await self.dismiss(True)
