import logging
import sys
from argparse import ArgumentParser

import uvicorn
from rich.logging import RichHandler

from bushido import __version__
from bushido.conf import DEFAULT_PORT
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
