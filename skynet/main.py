# general imports
import datetime
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.reactive import var
from textual.containers import Vertical, Horizontal
from rich.text import Text

import config
from unitproc import StringProcessor
# project imports
from utils import utilities
from txscreens import helpscreen, unitlog, timetable
from txwidgets import clock


class Skynet(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('t', 'toggle_tree', 'Toggle Tree'),
                ('g', 'unit_timeline', 'TimeLine'),
                ('l', 'log_unit', 'Log')]

    show_tree = var(True)

    def watch_show_tree(self, show_tree):
        self.set_class(show_tree, '-show-tree')

    def __init__(self):
        super().__init__()
        self.string_processor = StringProcessor(config.emojis)
        self.unit_retrievers = utilities.load_unit_retrievers(config.emojis)

    def compose(self) -> ComposeResult:
        yield Header()
        yield clock.Clock()
        with Horizontal():
            yield Tree('', id='tree-view')
        yield Footer()

    def on_mount(self):
        self.build_tree()

    def action_toggle_tree(self):
        self.show_tree = not self.show_tree

    def action_help(self):
        self.app.push_screen(helpscreen.HelpScreen())

    def action_log_unit(self):
        self.app.push_screen(unitlog.UnitLog(self.string_processor))

    def action_unit_timeline(self):
        self.app.push_screen(timetable.TimeTable(self.unit_retrievers))

    def build_tree(self) -> None:
        tree = self.query_one(Tree)
        tree.root.expand()

        def add_node(name, node, data):
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
            if isinstance(data, dict):
                node.label = Text(name)
                for key, value in data.items():
                    new_node = node.add('')
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                if isinstance(name, datetime.datetime):
                    node.label = Text(datetime.datetime.strftime(name, '%d.%m.%y %H:%M'))
                else:
                    node.label = name

                for index, value in enumerate(data):
                    new_node = node.add('')
                    add_node(str(index), new_node, value)
            else:
                node.allow_expand = False
                if name:
                    if isinstance(data, lifts.LiftsUnit):
                        data_str = str(data.liftsset)
                    elif isinstance(data, cali.CaliUnit):
                        data_str = str(data.caliset)
                    elif isinstance(data, wimhof.WimhofUnit):
                        data_str = str(data.wimhofround)
                    else:
                        data_str = str(data)

                    label = Text.assemble(
                        Text.from_markup(f'[b]{name}[/b] = ', style='blue'),
                        data_str, style='cyan')

                    #Text.from_markup(f"[b]{name}[/b]="), self.highlighter(
                    #self.unit2string(data)
                    #)
                else:
                    label = Text(repr(data))
                node.label = label

        #add_node(self.mod.mod_name.capitalize(), tree.root, self.mod.dt2units)


if __name__ == '__main__':
    app = Skynet()
    app.run()
