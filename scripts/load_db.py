from collections import defaultdict
import json
import re

# project imports
from bushido.exceptions import ValidationError
from bushido.data.conn import session_factory
from bushido.service.db_init import db_init
from bushido.service.log import LogService
from bushido.service.unit import BaseUnitService


def main():
    with open("units_2023-01-01_2025-05-02.json") as f:
        data = json.load(f)
    db_init()
    with session_factory.get_session_context() as session:
        service = LogService.from_session(session)
        us = BaseUnitService.from_session(session)

    errors = defaultdict(list)
    for unit in data:
        if unit["unit_name"] in ["study", "work", "reading"]:
            continue
        emoji = us.get_emoji_for_unit(unit["unit_name"])
        local_dt = re.sub(
            r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})",
            r"\1.\2.\3-\4\5",
            unit["local_datetime"],
        )
        try:
            text = " ".join([emoji, "--dt", local_dt, unit["payload"]])
        except:
            errors[unit["unit_name"]].append(unit["payload"])
            continue

        try:
            service.log_unit(text)
        except ValidationError:
            errors[unit["unit_name"]].append(unit["payload"])
            continue
        except KeyError:
            errors[unit["unit_name"]].append(unit["payload"])
            continue

    for k, v in errors.items():
        print(k)
        print("------")


if __name__ == "__main__":
    main()
