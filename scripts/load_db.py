import json
import sys
from typing import Any

from citadel.conf import get_db_url
from citadel.persistence import SessionFactory
from citadel.persistence.repos import AdminRepo
from citadel.schema.auth import RegisterRequest
from citadel.service import log_unit

UNIT_NAMES = [
    "strength",
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
    db_url = get_db_url()
    sf = SessionFactory(db_url=db_url)
    request = RegisterRequest(username='', email="np.javet@gmail.com", password="yo")

    with sf.session() as session:
        repo = AdminRepo(session)
        spartan = repo.create_spartan(request)
        session.commit()
        for unit in data:
            line = unit["line"]
            try:
                log_unit(line, session, spartan)
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