import logging
import sys
from argparse import ArgumentParser

from rich.logging import RichHandler
from sqlalchemy import Engine

from bushido import __version__
from bushido.conf import UnitType
from bushido.db.model import Base
from bushido.db.sf import SessionFactory
from bushido.dtypes import UnitRegistration
from bushido.registry import UNIT_REGISTRY
from bushido.service import UnitService
from bushido.tui.tui import BushidoApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument(
        "--tui", action="store_true", default=True, help="run Textual App "
    )
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


def build_unit_registry() -> dict[str, UnitRegistration]:
    for unit_type in UnitType:
        pass


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"bushido {__version__}")
        sys.exit(0)

    elif args.tui:
        sf = SessionFactory()
        init_db(engine=sf.engine)
        unit_service = UnitService(registry=UNIT_REGISTRY)
        BushidoApp(sf, unit_service).run()


if __name__ == "__main__":
    main()
