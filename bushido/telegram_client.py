import datetime
import sys
import os
from dataclasses import dataclass, field
import pytz
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
from dotenv import find_dotenv, load_dotenv
import logging


logger = logging.getLogger(__name__)


class AsyncTelegramClient(TelegramClient):
    def __init__(self, session='anon'):
        super().__init__(session, *self.get_api_keys())

    @staticmethod
    def get_api_keys():
        env_path = find_dotenv()
        if not env_path:
            print('create an .env file with api keys')
            sys.exit(1)
        load_dotenv(env_path)
        api_id = int(os.getenv('API_ID'))
        api_hash = os.getenv('API_HASH')
        return api_id, api_hash

    async def fetch_missed_messages(self, chat, last_message_id):
        if last_message_id is None:
            return

        history = await self(GetHistoryRequest(peer=chat,
                                               offset_id=last_message_id,
                                               offset_date=None,
                                               add_offset=0,
                                               limit=64,
                                               max_id=0,
                                               min_id=last_message_id + 1,
                                               hash=0))


class T800(AsyncTelegramClient):
    def __init__(self, session='bot', umanager=None):
        super().__init__(session)
        self.um = umanager
        self.add_event_handler(self.msg_recv_handler,
                               NewMessage(incoming=True))

    @staticmethod
    def get_bot_token():
        bot_token = os.getenv('BOT_TOKEN')
        if bot_token is None:
            print('define a BOT_TOKEN in .env')
            sys.exit(1)
        return bot_token

    async def start_bot(self):
        # TODO 'class telegram client does not define __await__ warning
        await self.start(bot_token=self.get_bot_token())

    async def msg_recv_handler(self, event):
        processing_result = self.um.process_string(event.message.message)
        if processing_result.success:
            tg_message_data = self.construct_telegram_message_data(event)
            self.um.save_unit_data(tg_message_data)
            await event.reply(processing_result.msg)
        else:
            await event.reply('FAIL: ' + processing_result.msg)

    @staticmethod
    def construct_telegram_message_data(event):
        log_time = event.message.date.astimezone(pytz.timezone('CET'))
        unix_timestamp = event.message.date.timestamp()
        tg = TelegramMessage(msg_id=event.message.id,
                             from_id=event.message.sender.id,
                             to_id=event.message.peer_id.user_id,
                             log_time=log_time,
                             unix_timestamp=unix_timestamp)
        return tg


@dataclass
class TelegramMessage:
    msg_id: int
    from_id: int
    to_id: int
    log_time: datetime.datetime
    unix_timestamp: float
    emoji_payload: str = field(init=False)
    comment: str | None = field(init=False)

    def set_data(self, emoji_payload, comment):
        self.emoji_payload = emoji_payload
        self.comment = comment
