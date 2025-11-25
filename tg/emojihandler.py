# general imports
import telegram
import telegram.ext as te
import time
import datetime
import re

import config


class EmojiHandler(te.BaseHandler):
    """
    Telegram Handler
    """
    def __init__(self, unit_manager):
        super().__init__(callback=self.emoji_handler)
        self.um = unit_manager
        self.regex = self.compute_regex()

    @staticmethod
    def compute_regex():
        """
        :return: | separated regex of emoticons keys
        """
        keys = [re.escape(emoji) for emoji in config.emojis.keys()]
        # since telegram uses different encoding for laptop and phone
        tgkeys = [re.escape(e.decode()) for e in config.single2double.keys()]
        return '|'.join(keys + tgkeys)

    async def emoji_handler(self, update: telegram.Update, context: te.CallbackContext):
        print('EMOJI HANDLER: ', update.message.text, '\ncontext args:', context.args, '\n')
        user_id = update.message.from_user.id
        recv_time = self.set_local_time(update.message.date)

        res = self.um.process_string(input_string=context.args,
                                     user_id=user_id,
                                     recv_time=recv_time)
        if res.success:
            ans = 'Unit confirmed!'
        else:
            ans = res.error
        await update.message.reply_text(ans, parse_mode='Markdown')

    def check_update(self, update: telegram.Update):
        """

        :param update:
        :return:
        """
        return re.match(self.regex, update.message.text)

    async def handle_update(self, update, dispatcher, check_result, context=None):
        """

        :param update:
        :param dispatcher:
        :param check_result:
        :param context:
        :return:
        """

        words = update.message.text.split()
        key = words[0].encode()
        try:
            key = config.single2double[key]
        except KeyError:
            pass
        if not key.decode() in self.um.emoji2proc.keys():
            return await update.message.reply_text('Space separate your input!')
        else:
            context.args = re.sub(words[0], key.decode(), update.message.text)
            return await self.callback(update, context)

    @staticmethod
    def set_local_time(message_date):
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - \
            datetime.datetime.utcfromtimestamp(now_timestamp)
        # TODO really weird, it is of type datetime, but in the datebase
        #  it is recorded as a string, why? so I need to convert it again
        lt0 = message_date + offset
        recv_time = datetime.datetime(lt0.year, lt0.month, lt0.day,
                                      lt0.hour, lt0.minute, lt0.second)
        return recv_time

