# general imports
import datetime

from emojis import emojis
from rich.text import Text

# project imports
from screens import helpscreen, unitlog
from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import *


class Nautilus(App):
    # CSS_PATH = 'main.css'

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("h", "help", "Help"),
        ("t", "toggle_tree", "Toggle Tree"),
        ("g", "unit_timeline", "TimeLine"),
        ("l", "log_unit", "Log"),
    ]

    show_tree = var(True)

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Tree("", data=0, id="unit-tree")
        yield TextArea()
        yield Button("Weights", id="weights")
        # yield clock.Clock()
        with Collapsible(title="Squat"):
            yield Label("yo")
        yield Collapsible(title="Deadlift")
        yield Rule()
        # yield stats.LiftStats(core.ugn2un2umoji['lifts'].values())

        # yield stats.WimhofStats(mnemosyne.ugn2un2umoji['wimhof']['wimhof'])
        # yield stats.CardioStats(mnemosyne.ugn2un2umoji['cardio'])
        yield Footer()

    def watch_show_tree(self, show_tree):
        self.set_class(show_tree, "-show-tree")

    def on_mount(self):
        self.build_tree()

    def build_tree(self):
        def add_node(name, node, data):
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
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


if __name__ == "__main__":
    try:
        import secconf
        from apx.db import User

        user = User.create(user_id=secconf.noe_id)
    except:
        pass
    app = Nautilus()
    app.run()
