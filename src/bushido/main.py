import logging
import sys
from argparse import ArgumentParser

from rich.logging import RichHandler

from bushido import __version__
from bushido.categories import LogUnitService
from bushido.categories.db import SessionFactory
from bushido.tui.tui import BushidoApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument(
        "--tui", action="store_true", default=True, help="run Textual App "
    )
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"bushido {__version__}")
        sys.exit(0)

    elif args.tui:
        sf = SessionFactory()
        # TODO all orm tables must have been imported already
        sf.init_db()
        log_unit_service = LogUnitService()
        BushidoApp(sf, log_unit_service).run()


if __name__ == "__main__":
    main()
