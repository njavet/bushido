from enum import StrEnum

GYM_UNIT_SETTINGS = {
    "kyokushin": b"\xf0\x9f\xa5\x8b".decode(),
    "grappling": b"\xf0\x9f\xa5\x8b".decode(),
    "lifting": b"\xf0\x9f\xa6\x8d".decode(),
}


CARDIO_UNIT_SETTINGS = {
    "running": b"\xf0\x9f\xaa\x96".decode(),
    "skipping": b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
    "swimming": b"\xf0\x9f\xa6\x88".decode(),
}


LIFTING_UNIT_SETTINGS = {
    "squat": b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
    "deadlift": b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
    "benchpress": b"\xf0\x9f\x9b\xab".decode(),
    "overheadpress": b"\xf0\x9f\x9a\x81".decode(),
    "rows": b"\xf0\x9f\x90\xa2".decode(),
    "curls": b"\xf0\x9f\xa6\xbe".decode(),
}


WIMHOF_UNIT_SETTINGS = {
    "wimhof": b"\xf0\x9f\xaa\x90".decode(),
}


class UnitCategory(StrEnum):
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    gym = "gym"
    wimhof = "wimhof"


DEFAULT_CATEGORIES: tuple[str, ...] = (
    "cardio",
    "lifting",
    "gym",
    "wimhof",
)
