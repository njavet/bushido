import json
import sys
from typing import Any

from bushido.infra.db import SessionFactory
from bushido.service.unit_load import UnitService

UNIT_NAMES = [
    "barbell",
    "kyokushin",
    "boxing",
    "grappling",
    "running",
    "swimming",
    "skipping",
    "squat",
    "deadlift",
    "benchpress",
    "overheadpress",
]


def load_db(data: list[Any]) -> None:
    sf = SessionFactory()
    sf.init_db()
    lus = UnitService()
    with sf.session() as session:
        for unit in data:
            line = unit["line"]
            unit_name = line.split()[0]
            if unit_name not in UNIT_NAMES:
                continue
            error = lus.log_unit(line, session)
            if error:
                print("ERROR", error, "line", line)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <json_file>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)

    load_db(data)


if __name__ == "__main__":
    main()
