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
import umanager
from utils import utilities
import txscreens
import txwidgets


class Skynet(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('g', 'timetable', 'TimeTable'),
                ('r', 'lifting', 'Res'),
                ('w', 'wimhof', 'Wimhof'),
                ('s', 'study', 'Study'),
                ('l', 'log_unit', 'Log')]

    CSS_PATH = 'skynet.tcss'

    def __init__(self):
        super().__init__()
        self.um = umanager.UManager()

    def compose(self) -> ComposeResult:
        # yield Header()
        yield txwidgets.binclock.Binclock()
        yield Rule()
        yield txwidgets.loghistory.LogHistory(secconf.user_id)
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )
        yield Footer()

    def action_help(self):
        self.app.push_screen(txscreens.helpscreen.HelpScreen())

    def action_log_unit(self):
        self.app.push_screen(txscreens.unitlog.UnitLog(secconf.user_id,
                                                       self.um))

    def action_timetable(self):
        self.app.push_screen(txscreens.timetable.TimeTable(secconf.user_id,
                                                           self.um.modname2stats))

    def action_lifting(self):
        self.app.push_screen(txscreens.lifting.LiftingScreen(secconf.user_id,
                                                             self.um.modname2stats))

    def action_wimhof(self):
        self.app.push_screen(txscreens.wimhof.WimhofScreen(secconf.user_id,
                                                           self.um.modname2stats['wimhof']))


if __name__ == '__main__':
    app = Skynet()
    app.run()
