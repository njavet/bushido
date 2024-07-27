import datetime
import pytz
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
import logging

# project imports
logger = logging.getLogger(__name__)


class TgCom:
    def __init__(self, um):
        self.um = um
        load_dotenv()
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash = os.getenv('API_HASH')
        self.bot_token = os.getenv('T800_TOKEN')
        # TODO find a better solution
        data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
        self.t800_session = os.path.join(data_dir, 't800.session')
        self.agent_session = os.path.join(data_dir, 'bushido.session')

        self.tg_agent = TelegramClient(self.agent_session,
                                       self.api_id,
                                       self.api_hash)
        self.tg_bot = self.setup_bot()

    def setup_bot(self):
        tg_bot = TelegramClient(self.t800_session,
                                self.api_id,
                                self.api_hash)
        tg_bot.add_event_handler(self.msg_recv_handler,
                                 NewMessage(incoming=True))
        return tg_bot

    async def msg_recv_handler(self, event):
        if event.message.reply_to is not None:
            return

        budoka_id, timestamp = self.extract_ids_and_time(event.message)
        ans = self.um.log_unit(budoka_id, timestamp, event.message.message)
        await event.reply(ans)

    async def start_bot(self):
        # TODO 'class telegram client does not define __await__ warning
        await self.tg_bot.start(bot_token=self.bot_token)

    @staticmethod
    def extract_ids_and_time(message):
        timestamp = message.date.timestamp()
        try:
            from_id = message.from_id.user_id
        except AttributeError:
            from_id = message.sender.id
        return from_id, timestamp

    async def fetch_missed_messages(self, chat):
        # TODO when the -dt option is used, this can fail
        last_message_timestamp = db.get_last_timestamp(db.get_me())
        print('last timestamp', last_message_timestamp)
        print('last utc time', datetime.datetime.fromtimestamp(last_message_timestamp,
                                                               pytz.timezone('utc')))
        print('last local time', datetime.datetime.fromtimestamp(last_message_timestamp,
                                                                 pytz.timezone('Europe/Zurich')))
        all_messages = await self.tg_agent.get_messages(chat, limit=32)
        messages = []
        for msg in all_messages:
            # unix utc timestamp
            cond0 = msg.date.timestamp() > last_message_timestamp
            cond1 = msg.reply_to is None
            if cond0 and cond1:
                print('msg', msg)
                messages.append(msg)
        return messages

    async def process_missed_messages(self, chat):
        messages = await self.fetch_missed_messages(chat)
        for msg in messages:
            budoka_id, timestamp = self.extract_ids_and_time(msg)
            ans = self.um.log_unit(budoka_id, timestamp, msg.message)
            await msg.reply(ans)
