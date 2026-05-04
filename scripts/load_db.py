import json
import sys
from typing import Any

from bushido.categories.db import SessionFactory
from bushido.categories.unit_service import UnitService


def load_db(data: list[Any]) -> None:
    sf = SessionFactory()
    sf.init_db()
    lus = UnitService()
    with sf.session() as session:
        for unit in data:
            line = unit["line"] + " --dt " + unit["local_datetime"]
            lus.log_unit(line, session)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <json_file>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)

    load_db(data)


if __name__ == "__main__":
    main()
