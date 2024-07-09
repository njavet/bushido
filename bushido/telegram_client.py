import datetime
import pytz
from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
import logging

# project imports
import settings
import db

logger = logging.getLogger(__name__)


class AsyncTelegramClient(TelegramClient):
    def __init__(self, session='anon', umanager=None):
        super().__init__(session, settings.api_id, settings.api_hash)
        self.um = umanager

    @staticmethod
    def extract_ids_and_time(message):
        unix_timestamp = message.date.timestamp()
        try:
            from_id = message.from_id.user_id
        except AttributeError:
            from_id = message.sender.id
        return from_id, unix_timestamp

    async def fetch_missed_messages(self, chat):
        # TODO when the -dt option is used, this can fail
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

    async def start_bot(self):
        # TODO 'class telegram client does not define __await__ warning
        await self.start(bot_token=settings.bot_token)

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
