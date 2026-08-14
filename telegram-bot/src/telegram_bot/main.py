import asyncio
import os

from telethon import TelegramClient

from telegram_bot.api_client import BushidoApiClient
from telegram_bot.bot import BushidoTelegramBot


async def async_main() -> None:
    api_id = int(os.environ["TELEGRAM_API_ID"])
    api_hash = os.environ["TELEGRAM_API_HASH"]
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]

    api_client = BushidoApiClient(
        base_url=os.getenv(
            "BUSHIDO_API_URL",
            "http://localhost:8000",
        )
    )

    telegram = TelegramClient(
        "bushido-bot",
        api_id,
        api_hash,
    )

    await telegram.start(bot_token=bot_token)

    BushidoTelegramBot(
        telegram_client=telegram,
        api_client=api_client,
    )

    try:
        await telegram.run_until_disconnected()
    finally:
        await api_client.close()
        await telegram.disconnect()


def main() -> None:
    asyncio.run(async_main())
