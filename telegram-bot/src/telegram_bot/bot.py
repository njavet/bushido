from telethon import TelegramClient, events
from telethon.events import NewMessage

from telegram_bot.api_client import BushidoApiClient


class BushidoTelegramBot:
    def __init__(
        self,
        telegram_client: TelegramClient,
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
        event: NewMessage.Event,
    ) -> None:
        text = event.raw_text.strip()

        if text == "/units":
            await self._handle_units(event)
            return

        if text.startswith("/load "):
            await self._handle_load(event, text)
            return

        if text.startswith("/log "):
            await self._handle_log(event, text)
            return

        await event.reply(
            "Commands:\n/units\n/log <unit command>\n/load <unit command>"
        )

    async def _handle_units(
        self,
        event: NewMessage.Event,
    ) -> None:
        settings = await self._api.load_unit_settings()

        lines = [f"{setting.name} [{setting.category}]" for setting in settings]

        await event.reply("\n".join(lines))

    async def _handle_log(
        self,
        event: NewMessage.Event,
        text: str,
    ) -> None:
        raw = text.removeprefix("/log ").strip()

        # Your existing parser should convert raw input into
        # the correct discriminated LogUnitRequest.
        request = parse_log_unit_request(raw)

        result = await self._api.log_unit(request)

        await event.reply(f"Logged unit: {result}")

    async def _handle_load(
        self,
        event: NewMessage.Event,
        text: str,
    ) -> None:
        raw = text.removeprefix("/load ").strip()

        request = parse_load_unit_request(raw)

        units = await self._api.load_units(request)

        await event.reply(str(units))
