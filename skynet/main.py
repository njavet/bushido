# general imports
import datetime
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.reactive import var
from textual.containers import Vertical, Horizontal
from rich.text import Text

import config
import secconf

from unitproc import StringProcessor
# project imports
from utils import utilities
from txscreens import helpscreen, unitlog, timetable, resistance
import txwidgets


class Skynet(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('t', 'toggle_tree', 'Toggle Tree'),
                ('g', 'unit_timeline', 'TimeLine'),
                ('r', 'res', 'Res'),
                ('l', 'log_unit', 'Log')]

    CSS_PATH = 'skynet.tcss'
    show_tree = var(True)

    def watch_show_tree(self, show_tree):
        self.set_class(show_tree, '-show-tree')

    def __init__(self):
        super().__init__()
        self.string_processor = StringProcessor(config.emojis)
        self.unit_retrievers = utilities.load_unit_retrievers(config.emojis)

    def compose(self) -> ComposeResult:
        # yield Header()
        yield txwidgets.Binclock()
        yield Rule()
        yield Tree('Units', id='tree-view')
        yield Placeholder()
        yield Placeholder()
        yield Placeholder()

        yield Footer()

    def on_mount(self):
        self.build_tree()

    def action_toggle_tree(self):
        self.show_tree = not self.show_tree

    def action_help(self):
        self.app.push_screen(helpscreen.HelpScreen())

    def action_log_unit(self):
        self.app.push_screen(unitlog.UnitLog(secconf.user_id,
                                             self.string_processor))

    def action_unit_timeline(self):
        self.app.push_screen(timetable.TimeTable(secconf.user_id,
                                                 self.unit_retrievers))

    def action_res(self):
        self.app.push_screen(resistance.ResistanceScreen(secconf.user_id,
                                                         self.unit_retrievers))

    def build_tree(self) -> None:
        tree = self.query_one('#tree-view', Tree)
        tree.root.expand()

        for module_name, ur in self.unit_retrievers.items():
            dix = ur.datetime2unit(secconf.user_id)
            utilities.add_tree_node(module_name, tree.root.add(''), dix)


if __name__ == '__main__':
    app = Skynet()
    app.run()
