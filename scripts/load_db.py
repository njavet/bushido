import json
import os
import sys
from typing import Any

from dotenv import load_dotenv

from bushido_server.persistence import SessionFactory
from bushido_server.service import log_unit

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

load_dotenv()
BUSHIDO_DB_URL = os.environ.get("BUSHIDO_DB_URL", "sqlite:///bushido.db")


def load_db(data: list[Any]) -> None:
    sf = SessionFactory(db_url=BUSHIDO_DB_URL)
    with sf.session() as session:
        for unit in data:
            line = unit["line"]
            unit_name = line.split()[0]
            if unit_name not in UNIT_NAMES:
                continue
            try:
                log_unit(line, session)
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