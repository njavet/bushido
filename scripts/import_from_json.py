import datetime
import json
import sys
from typing import Any
from zoneinfo import ZoneInfo


def convert_tg_export(
    json_data: dict[str, Any], local_timezone: ZoneInfo = ZoneInfo("Europe/Zurich")
) -> list[Any]:
    """
    this converts jsondata that was exported from telegram
    """
    lst = []
    for message in json_data["messages"]:
        msg_text = message["text"]
        reply = "reply_to_message_id" in message
        if msg_text and not reply:
            # this is CET time when I export it from telegram
            dt_str = message["date"]
            dt_format = "%Y-%m-%dT%H:%M:%S"
            naive_dt = datetime.datetime.strptime(dt_str, dt_format)
            local_dt = naive_dt.replace(tzinfo=local_timezone)
            local_dt_str = datetime.datetime.strftime(local_dt, "%Y%m%d-%H%M")
            dix = {
                "line": msg_text,
                "local_datetime": local_dt_str,
            }
            lst.append(dix)
    return lst


def convert_tg_export_to_file(json_data: dict[str, Any]) -> None:
    res = convert_tg_export(json_data)
    with open("converted.json", "w") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <json_file>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)

    convert_tg_export_to_file(data)


if __name__ == "__main__":
    main()
