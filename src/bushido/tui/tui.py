from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Key
from textual.suggester import Suggester, SuggestionReady
from textual.widgets import Footer, Input, Rule, TextArea, Tree
from textual_image.widget import Image as ImageWidget

from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import Err, Ok, Warn
from bushido.modules.factory import Factory
from bushido.modules.timeline import fetch_display_units
from bushido.service.log_unit import log_unit
from bushido.tui.emojis import un2emoji
from bushido.tui.txwidgets.binary_clock import BinaryClock
from bushido.tui.txwidgets.unit_log import UnitLog


class BushidoApp(App[None]):
    BINDINGS = [
        ("q", "quit", "quit"),
        ("h", "help", "help"),
        ("t", "toggle_tree", "toggle tree"),
        ("g", "unit_timeline", "timeLine"),
        ("l", "log_unit", "log"),
    ]
    TITLE = "bushido"
    CSS_PATH = "main.tcss"

    def __init__(self, session_factory: SessionFactory, factory: Factory) -> None:
        super().__init__()
        self.sf = session_factory
        self.factory = factory
        with self.sf.session() as session:
            units = fetch_display_units(session)
        self.unit_log = UnitLog(units, un2emoji)

    def compose(self) -> ComposeResult:
        with Horizontal(id="status_bar"):
            yield ImageWidget("src/bushido/static/belts/black_belt.png", id="belt")
            yield ImageWidget("src/bushido/static/belts/rank.png", id="rank")
            yield BinaryClock(id="clock")
        yield Tree("", data=0, id="unit-tree")
        yield TextArea()
        yield TextInput(suggester=UnitSuggester(un2emoji))
        yield Rule()
        yield self.unit_log
        yield Footer()

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
