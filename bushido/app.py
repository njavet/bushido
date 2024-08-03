from textual.app import App, ComposeResult
from textual.widgets import Footer, LoadingIndicator

# project imports
from bushido.keikolib import UnitManager
from bushido.txscreens.helpscreen import HelpScreen
from bushido.txscreens.tx_unit_mgr import TxUnitManager
from bushido.txwidgets.unithistory import UnitHistory


class Bushido(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('l', 'log_unit', 'log')]

    # TODO clean config
    CSS_PATH = 'assets/main.tcss'

    def __init__(self):
        super().__init__()
        self.um = UnitManager()
        self.unit_history = UnitHistory(self.um)

    def compose(self) -> ComposeResult:
        yield self.unit_history
        yield Footer()

    def action_help(self):
        self.app.push_screen(HelpScreen(self.um))

    def action_log_unit(self):
        self.app.push_screen(TxUnitManager(self.um))


if __name__ == '__main__':
    app = Bushido()
    app.run()
