"""
import logging
import sys
from argparse import ArgumentParser

import uvicorn
from rich.logging import RichHandler

from bushido import __version__
from bushido.core.conf import DEFAULT_PORT
from bushido.tui.tui import BushidoApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--tui", action="store_true", help="run Textual App ")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"bushido {__version__}")
        sys.exit(0)

    elif args.tui:
        BushidoApp().run()

    elif args.dev:
        uvicorn.run(
            "bushido.web.web:create_app",
            port=DEFAULT_PORT,
            reload=True,
            factory=True,
            log_level="debug",
        )
    else:
        uvicorn.run(
            "bushido.web.web:create_app",
            port=DEFAULT_PORT,
            factory=True,
            log_level="info",
        )

"""

from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Static
from textual_image.widget import Image as ImageWidget  # from textual-image


class BeltCard(Vertical):
    def __init__(self, belt_name: str, image_path: Path) -> None:
        super().__init__()
        self.belt_name = belt_name
        self.image_path = image_path

    def compose(self) -> ComposeResult:
        yield ImageWidget(str(self.image_path))
        yield Static(self.belt_name, classes="belt-name")


class BushidoApp(App[None]):
    CSS = """
    Screen {
        layout: vertical;
    }

    #header {
        padding: 1 2;
        height: 3;
        content-align: left middle;
    }

    #belt-row {
        height: auto;
        padding: 1 2;
    }

    BeltCard {
        width: 20;
        height: auto;
        border: round $accent;
        padding: 1;
        align: center middle;
    }

    .belt-name {
        content-align: center middle;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Bushido Admin Panel", id="header")
        yield Horizontal(
            BeltCard("White Belt", Path("black_belt.png")),
            id="belt-row",
        )
        yield Footer()


if __name__ == "__main__":
    BushidoApp().run()
