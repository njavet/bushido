import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, LoadingIndicator

# project imports
from unit_manager import UnitManager
from telegram_client import T800, AsyncTelegramClient
from txscreens.helpscreen import HelpScreen
from txscreens.login import LoginScreen
from txscreens.unitlog import UnitLog
from txwidgets.unithistory import UnitHistory
import db
import config


class Bushido(App):

    BINDINGS = [('q', 'quit', 'Quit'),
                ('h', 'help', 'Help'),
                ('l', 'log_unit', 'Log')]

    # TODO clean config
    CSS_PATH = '../stylesheets/main.tcss'

    def __init__(self):
        super().__init__()
        self.um = UnitManager(config.emojis)
        self.t800 = None
        self.unit_history = UnitHistory()
        self.tg_client = AsyncTelegramClient(session=config.bushido_session,
                                             umanager=self.um)

    def init_unit_tables(self):
        models = []
        for unit_module in self.um.unit_modules.values():
            models.append(unit_module.subunit_model)
        db.init_storage(models)

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        yield Footer()

    async def check_authorization(self):
        await self.tg_client.connect()
        is_authorized = await self.tg_client.is_user_authorized()
        if is_authorized:
            await self.query_one(LoadingIndicator).remove()
            await self.mount(self.unit_history, before=self.query_one(Footer))
            await self.tg_client.fetch_missed_messages('csm101_bot')
        else:
            await self.push_screen(LoginScreen(self.tg_client), self.check_login)

    def check_login(self, user):
        # TODO check failure
        db.add_agent(user.id, user.first_name, is_me=True)
        self.query_one(LoadingIndicator).remove()
        self.mount(UnitHistory(), before=self.query_one(Footer))

    async def on_mount(self):
        await asyncio.create_task(self.check_authorization())
        self.t800 = T800(session=config.t800_session, umanager=self.um)
        await self.t800.start_bot()

    def action_help(self):
        self.app.push_screen(HelpScreen(config.emojis))

    def action_log_unit(self):
        self.app.push_screen(UnitLog(self.um.emoji2proc, self.tg_client))


if __name__ == '__main__':
    app = Bushido()
    app.run()
