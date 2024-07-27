import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, LoadingIndicator

# project imports
from bushido import UnitManager
from tgcom import TgCom
from txscreens.helpscreen import HelpScreen
from txscreens.login import LoginScreen
from txscreens.tx_unit_mgr import TxUnitManager
from txwidgets.unithistory import UnitHistory
import db


class Bushido(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('u', 'manage_units', 'Unit')]

    # TODO clean config
    CSS_PATH = 'assets/main.tcss'

    def __init__(self):
        super().__init__()
        self.um = UnitManager()
        self.unit_history = UnitHistory()
        self.tg_com = TgCom(self.um)

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

    def check_login(self, user):
        # TODO check failure
        db.add_budoka(user.id, user.first_name, is_me=True)
        self.query_one(LoadingIndicator).remove()
        self.mount(UnitHistory(), before=self.query_one(Footer))

    async def on_mount(self):
        await self.tg_com.start_bot()
        await asyncio.create_task(self.check_authorization())

    def action_help(self):
        self.app.push_screen(HelpScreen(config.emojis))

    def action_manage_units(self):
        def units_changed(changed: bool) -> None:
            if changed:
                self.unit_history.update_history()

        self.app.push_screen(TxUnitManager(self.um,
                                           self.tg_com.tg_agent),
                             units_changed)


if __name__ == '__main__':
    app = Bushido()
    app.run()
