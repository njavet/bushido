# general imports
import datetime
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.reactive import var
from textual.containers import Vertical, Horizontal
from rich.text import Text

# project imports
import config
import secconf
import unit_manager
from utils import utilities
import txscreens
import txwidgets


class Skynet(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('t', 'toggle_tree', 'Toggle Tree'),
                ('g', 'timetable', 'TimeTable'),
                ('r', 'res', 'Res'),
                ('w', 'wimhof', 'Wimhof'),
                ('s', 'study', 'Study'),
                ('l', 'log_unit', 'Log')]

    CSS_PATH = 'skynet.tcss'
    show_tree = var(True)

    def watch_show_tree(self, show_tree):
        self.set_class(show_tree, '-show-tree')

    def __init__(self):
        super().__init__()
        self.um = unit_manager.UnitManager()

    def compose(self) -> ComposeResult:
        # yield Header()
        yield txwidgets.binclock.Binclock()
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
        self.app.push_screen(txscreens.helpscreen.HelpScreen())

    def action_log_unit(self):
        self.app.push_screen(txscreens.unitlog.UnitLog(secconf.user_id,
                                                       self.um))

    def action_timetable(self):
        self.app.push_screen(txscreens.timetable.TimeTable(secconf.user_id,
                                                           self.um.modname2stats))

    def action_res(self):
        self.app.push_screen(txscreens.resistance.ResistanceScreen(secconf.user_id,
                                                                   self.um.modname2stats))

    def action_wimhof(self):
        self.app.push_screen(txscreens.wimhof.WimhofScreen(secconf.user_id,
                                                           self.um.modname2stats['wimhof']))

    def build_tree(self) -> None:
        tree = self.query_one('#tree-view', Tree)
        tree.root.expand()

        for module_name, ur in self.um.modname2stats.items():
            dix = ur.datetime2unit(secconf.user_id)
            utilities.add_tree_node(module_name, tree.root.add(''), dix)


if __name__ == '__main__':
    app = Skynet()
    app.run()
