import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, LoadingIndicator, Button
from textual.containers import Horizontal, Vertical
import os
import sys

# project imports
from bushido.services import UnitManager
from bushido.db import DatabaseManager
from bushido.tgcom import TgCom
from bushido.txscreens.helpscreen import HelpScreen
from bushido.txscreens.login import LoginScreen
from bushido.txscreens.tx_unit_mgr import TxUnitManager
from bushido.txwidgets.unithistory import UnitHistory


class Bushido(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('m', 'manage_units', 'Unit')]

    # TODO clean config
    CSS_PATH = 'assets/main.tcss'

    def __init__(self):
        super().__init__()
        self.dbm = DatabaseManager('sqlite:///bushido.db')
        self.dbm.init_db()
        self.um = UnitManager(self.dbm)
        self.tg_com = TgCom(self.um)
        self.unit_history = UnitHistory(self.um)

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        yield Footer()

    async def check_authorization(self):
        # ConnectionError: Connection to Telegram failed 5 time(s)
        await self.tg_com.tg_agent.connect()
        is_authorized = await self.tg_com.tg_agent.is_user_authorized()
        if is_authorized:
            await self.query_one(LoadingIndicator).remove()
            await self.tg_com.process_missed_messages('csm101_bot')
            await self.mount(self.unit_history, before=self.query_one(Footer))
        else:
            await self.push_screen(LoginScreen(self.tg_com.tg_agent), self.check_login)

    def check_login(self):
        self.query_one(LoadingIndicator).remove()
        self.mount(self.unit_history, before=self.query_one(Footer))

    async def on_mount(self):
        await self.tg_com.start_bot()
        await asyncio.create_task(self.check_authorization())
        self.um.unit_logged.connect(self.unit_history.update_view)

    def on_button_pressed(self, event):
        pass

    def action_help(self):
        self.app.push_screen(HelpScreen(self.um))

    def action_manage_units(self):
        self.app.push_screen(TxUnitManager(self.um,
                                           self.tg_com.tg_agent))


if __name__ == '__main__':
    app = Bushido()
    app.run()

