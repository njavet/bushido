import datetime
import sys
import os
import pytz
from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
from dotenv import find_dotenv, load_dotenv
import logging

# project imports
import db

logger = logging.getLogger(__name__)


class AsyncTelegramClient(TelegramClient):
    def __init__(self, session='anon', umanager=None):
        super().__init__(session, *self.get_api_keys())
        self.um = umanager

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

    @staticmethod
    def extract_ids_and_time(message):
        log_time = message.date.astimezone(pytz.timezone('utc'))
        unix_timestamp = message.date.timestamp()
        try:
            from_id = message.from_id.user_id
        except AttributeError:
            from_id = message.sender.id

        return from_id, unix_timestamp

    async def fetch_missed_messages(self, chat):
        last_message_timestamp = db.get_last_timestamp(db.get_me())
        print('last timestamp', last_message_timestamp)
        print('last utc time', datetime.datetime.fromtimestamp(last_message_timestamp,
                                                               pytz.timezone('utc')))
        print('last local time', datetime.datetime.fromtimestamp(last_message_timestamp,
                                                               pytz.timezone('Europe/Zurich')))
        all_messages = await self.get_messages(chat, limit=32)
        messages = []
        for msg in all_messages:
            # unix utc timestamp
            cond0 = msg.date.timestamp() > last_message_timestamp
            cond1 = msg.reply_to is None
            if cond0 and cond1:
                print('msg', msg)
                messages.append(msg)

        for msg in messages:
            processing_result = self.um.process_string(msg.message)
            if processing_result.success:
                agent_id, unix_timestamp = self.extract_ids_and_time(
                    msg
                )
                self.um.save_unit_data(agent_id,
                                       unix_timestamp)
                await self.send_message('csm101_bot',
                                        processing_result.msg,
                                        reply_to=msg.id)
            else:
                await self.send_message('csm101_bot',
                                        'Fail: ' + processing_result.msg,
                                        reply_to=msg.id)


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
            agent_id, unix_timestamp = self.extract_ids_and_time(
                event.message
            )
            self.um.save_unit_data(agent_id,
                                   unix_timestamp)
            await event.reply(processing_result.msg)
        else:
            await event.reply('FAIL: ' + processing_result.msg)

