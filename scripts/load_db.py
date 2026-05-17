import json
import sys
from typing import Any

from bushido.db.sf import SessionFactory
from bushido.main import init_db
from bushido.registry import build_registry
from bushido.service import LogUnitService

UNIT_NAMES = [
    "lifting",
    "kyokushin",
    "boxing",
    "grappling",
    "cardio",
    "swimming",
    "skipping",
    "squat",
    "deadlift",
    "benchpress",
    "overheadpress",
]


def load_db(data: list[Any]) -> None:
    sf = SessionFactory()
    init_db(engine=sf.engine)
    lus = LogUnitService(registry=build_registry())
    with sf.session() as session:
        for unit in data:
            line = unit["line"]
            unit_name = line.split()[0]
            if unit_name not in UNIT_NAMES:
                continue
            try:
                lus.log_unit(line, session)
            except Exception as e:
                print(str(e))


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <json_file>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)

    load_db(data)


if __name__ == "__main__":
    main()
