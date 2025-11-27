from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Key
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import (
    Digits,
    Input,
    Markdown,
    Rule,
    TabbedContent,
    TabPane,
)

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Warn
from bushido.modules.factory import Factory
from bushido.modules.timeline import fetch_display_units
from bushido.service.log_unit import log_unit
from bushido.tui.containers.header import HeaderContainer


class BushidoApp(App[None]):
    BINDINGS = [
        Binding("q", "quit", "quit"),
        Binding("h", "help", "help"),
        Binding("t", "toggle_tree", "toggle tree"),
        Binding("g", "unit_timeline", "timeLine"),
        Binding("l", "log_unit", "log"),
    ]
    CSS_PATH = "main.tcss"

    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
        with self.sf.session() as session:
            units = fetch_display_units(session)

    def compose(self) -> ComposeResult:
        yield Rule()
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

        # yield TextArea()
        # yield Tree("", data=0, id="unit-tree")
        # yield TextInput(suggester=UnitSuggester(un2emoji))
        # yield self.unit_log

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value.strip()
        event.input.value = ""
        if not line:
            return

        with self.sf.session() as session:
            res = log_unit(line, self.factory, session)

        if isinstance(res, Ok):
            unit = res.value
            self.unit_log.update_view(unit)
        elif isinstance(res, Warn):
            print(res.message)
            pass
        elif isinstance(res, Err):
            print(res.message)
            pass

    def watch_show_tree(self, show_tree: Any) -> None:
        self.set_class(show_tree, "-show-tree")

    """
    def build_tree(self):
        def add_node(name, node, data):
            if isinstance(data, dict):
                if isinstance(name, str):
                    node.label = Text(name, style="cyan")
                if node.data < 2:
                    node.expand()
                for key, value in data.items():
                    new_node = node.add("", data=(node.data + 1))
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                if isinstance(name, datetime.datetime):
                    node.label = Text(
                        datetime.datetime.strftime(name, "%d.%m.%y %H:%M")
                    )
                else:
                    node.label = name

                for index, value in enumerate(data):
                    new_node = node.add("", data=(node.data + 1))
                    add_node(str(index), new_node, value)

            else:
                node.allow_expand = False
                if name:
                    try:
                        data_str = str(data.liftsset)
                    except:
                        data_str = str(data)

                    label = Text.assemble(
                        str(len(str(data))),
                        Text.from_markup(f"[b]{name}[/b] = ", style="blue"),
                        data_str,
                        style="cyan",
                    )
                else:
                    label = Text(repr(data))
                node.label = label

        tree = self.query_one(Tree)
        tree.root.expand()
        add_node("Units", tree.root, {})

    def action_log_unit(self):
        # TODO update other widgets after saving a unit
        self.app.push_screen(unitlog.UnitLog(self.string_processor))

    def action_help(self):
        self.app.push_screen(helpscreen.HelpScreen(emojis))

    def action_toggle_tree(self):
        self.show_tree = not self.show_tree

    def action_unit_timeline(self):
        self.app.push_screen(timeline.TimeLine())

    def on_button_pressed(self, event):
        if event.button.id == "weights":
            self.app.push_screen(weights.Weights())

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        rl = self.query_one("#response", RichLog)
        rl.clear()
        rl.write(msg.message)
        self.query_one(Input).action_delete_left_all()
        self.query_one(Input).action_delete_right_all()
"""


class UnitSuggester(Suggester):
    def __init__(self, emojis: dict[str, str]) -> None:
        super().__init__()
        self.emojis = emojis

    async def get_suggestion(self, value: str) -> str | None:
        es = [uname for uname, emoji in self.emojis.items() if uname.startswith(value)]
        if len(es) == 1:
            return es[0] + " "
        return None


class TextInput(Input):
    def __init__(self, suggester: UnitSuggester) -> None:
        super().__init__(suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
