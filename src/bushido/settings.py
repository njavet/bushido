from enum import StrEnum
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Europe/Zurich")

DAY_START_HOUR = 4

COMMENT_SEP = "#"

POINT_DIVISOR = 64


class Category(StrEnum):
    training = "training"
    gym = "gym"
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    wimhof = "wimhof"


UNIT_SETTINGS = {
    "kyokushin": {
        "emoji": b"\xf0\x9f\xa5\x8b",
        "unit": Category.training,
        "options": {},
        "flags": [],
    },
    "grappling": {
        "emoji": b"\xf0\x9f\xa5\x8b".decode(),
        "unit": Category.training,
        "options": {},
        "flags": [],
    },
    "boxing": {
        "emoji": b"\xf0\x9f\xa5\x8b".decode(),
        "unit": Category.training,
        "options": {},
        "flags": [],
    },
    "lifting": {
        "emoji": b"\xf0\x9f\xa6\x8d".decode(),
        "unit": Category.training,
        "options": {},
        "flags": [],
    },
    "running": {
        "emoji": b"\xf0\x9f\xaa\x96".decode(),
        "unit": Category.cardio,
        "options": {},
        "flags": [],
    },
    "skipping": {
        "emoji": b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
        "unit": Category.cardio,
        "options": {},
        "flags": [],
    },
    "swimming": {
        "emoji": b"\xf0\x9f\xa6\x88".decode(),
        "unit": Category.cardio,
        "options": {},
        "flags": [],
    },
    "squat": {
        "emoji": b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "deadlift": {
        "emoji": b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "benchpress": {
        "emoji": b"\xf0\x9f\x9b\xab".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "overheadpress": {
        "emoji": b"\xf0\x9f\x9a\x81".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "rows": {
        "emoji": b"\xf0\x9f\x90\xa2".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "curls": {
        "emoji": b"\xf0\x9f\xa6\xbe".decode(),
        "unit": Category.lifting,
        "options": {},
        "flags": [],
    },
    "wimhof": {
        "wimhof": b"\xf0\x9f\xaa\x90".decode(),
        "unit": Category.wimhof,
        "options": {},
        "flags": [],
    },
}
