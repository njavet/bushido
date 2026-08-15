from typing import Any, Protocol

from telethon import TelegramClient, events
from telethon.events import NewMessage

from telegram_bot.api_client import BushidoApiClient


class TelegramClientProtocol(Protocol):
    def add_event_handler(self, callback: object, event: object) -> None: ...


class TelegramEvent(Protocol):
    raw_text: str
    async def reply(self, message: str) -> object: ...


class BushidoTelegramBot:
    def __init__(
        self,
        telegram_client: TelegramClientProtocol,
        api_client: BushidoApiClient,
    ) -> None:
        self._telegram = telegram_client
        self._api = api_client

        self._register_handlers()

    def _register_handlers(self) -> None:
        self._telegram.add_event_handler(
            self._handle_message,
            events.NewMessage(incoming=True),
        )

    async def _handle_message(
        self,
        event: TelegramEvent,
    ) -> None:
        text = event.raw_text.strip()

        if text == "/units":
            await self._handle_units(event)
            return

        if text.startswith("/log "):
            await self._handle_log(event, text)
            return

        await event.reply(
            "Commands:\n/units\n/log <unit command>\n/load <unit command>"
        )

    async def _handle_units(
        self,
        event: TelegramEvent,
    ) -> None:
        settings = await self._api.load_unit_settings()

        lines = [f"{setting.name} [{setting.category}]" for setting in settings]

        await event.reply("\n".join(lines))

    async def _handle_log(
        self,
        event: TelegramEvent,
        text: str,
    ) -> None:
        request = text.strip()
        result = await self._api.log_unit(request)
        await event.reply(f"Logged unit: {result}")
