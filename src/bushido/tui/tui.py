from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Digits,
    Footer,
    Markdown,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.infra.db import SessionFactory
from bushido.service.log_unit import LogUnitService
from bushido.tui.containers.header import HeaderContainer
from bushido.tui.screens.helpscreen import HelpScreen
from bushido.tui.screens.log_unit import LogUnitScreen


class BushidoApp(App[None]):
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("h", "help", "help"),
        Binding("t", "toggle_tree", "toggle tree"),
        Binding("g", "unit_timeline", "timeLine"),
        Binding("l", "log_unit", "log"),
    ]
    CSS_PATH = "main.tcss"

    def __init__(
        self, session_factory: SessionFactory, log_unit_service: LogUnitService
    ) -> None:
        super().__init__()
        self.sf = session_factory
        self.log_unit_service = log_unit_service

    def compose(self) -> ComposeResult:
        yield HeaderContainer(
            "white",
            "renegade",
            Path("src/bushido/assets/belts/white_belt.png"),
            Path("src/bushido/assets/belts/rank.png"),
            id_="header",
        )
        yield Rule()
        with TabbedContent():
            with TabPane("|-"):
                yield Markdown("00")
            with TabPane("🥋"):
                yield Markdown("00")
            with TabPane("ℵ₀"):
                with TabbedContent():
                    with TabPane("squat"):
                        yield Markdown("11")
                    with TabPane("deadlift"):
                        yield Markdown("22")
                    with TabPane("deadlift"):
                        yield Markdown("33")
                    with TabPane("benchpress"):
                        yield Markdown("44")
                    with TabPane("overheadpress"):
                        yield Markdown("55")
            with TabPane("🤿"):
                with TabbedContent():
                    with TabPane("running"):
                        yield Markdown("66")
                    with TabPane("skipping"):
                        yield Digits("0x101")
            with TabPane("wimhof"):
                yield Markdown("77")
        yield Footer()

    def action_log_unit(self) -> None:
        # TODO update other widgets after saving a unit
        with self.sf.session() as session:
            self.app.push_screen(LogUnitScreen(self.log_unit_service, session))

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())

    def watch_show_tree(self, show_tree: Any) -> None:
        self.set_class(show_tree, "-show-tree")
