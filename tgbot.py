# general imports
import sys

# project imports
import secconf
import telegram
import telegram.ext as te

from tg.emojihandler import EmojiHandler
from umanager import UManager

"""
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
"""


async def hh(update, context):
    print(context.args[0].encode())


def main():
    try:
        application = te.ApplicationBuilder().token(secconf.token).build()
    except telegram.error.InvalidToken:
        print("invalid token! get a new token @BotFather")
        sys.exit(1)

    h = te.CommandHandler("help", hh)
    application.add_handler(h)

    um = UManager()
    eh = EmojiHandler(um)
    application.add_handler(eh)

    application.run_polling()


if __name__ == "__main__":
    main()
