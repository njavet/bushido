import pytest

from bushidolib.unit.base import RawUnit


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "some-unit",
            RawUnit(
                name="some-unit",
                tokens=(),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "running 1730",
            RawUnit(
                name="running",
                tokens=("1730",),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "athena 1730 45:00 gym 5.2",
            RawUnit(
                name="athena",
                tokens=("1730", "45:00", "gym", "5.2"),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "platon -x",
            RawUnit(
                name="platon",
                tokens=(),
                flags=["x"],
                options={},
                comment=None,
            ),
        ),
        (
            "kant -x -y -z",
            RawUnit(
                name="kant",
                tokens=(),
                flags=["x", "y", "z"],
                options={},
                comment=None,
            ),
        ),
        (
            "starcraft --avghr 140",
            RawUnit(
                name="starcraft",
                tokens=(),
                flags=[],
                options={"avghr": "140"},
                comment=None,
            ),
        ),
        (
            "jogging --avghr 140 --maxhr 175 --cal 500",
            RawUnit(
                name="jogging",
                tokens=(),
                flags=[],
                options={
                    "avghr": "140",
                    "maxhr": "175",
                    "cal": "500",
                },
                comment=None,
            ),
        ),
        (
            "running # easy run",
            RawUnit(
                name="running",
                tokens=(),
                flags=[],
                options={},
                comment="easy run",
            ),
        ),
        (
            "running 1730 45:00 # easy zone 2 run",
            RawUnit(
                name="running",
                tokens=("1730", "45:00"),
                flags=[],
                options={},
                comment="easy zone 2 run",
            ),
        ),
        (
            "running 1730 45:00 gym 16.4 -x --avghr 160 --maxhr 187 --cal 500 # hard",
            RawUnit(
                name="running",
                tokens=("1730", "45:00", "gym", "16.4"),
                flags=["x"],
                options={
                    "avghr": "160",
                    "maxhr": "187",
                    "cal": "500",
                },
                comment="hard",
            ),
        ),
        (
            "running --avghr 140 1730 -x 45:00 --cal 500 gym 5.2",
            RawUnit(
                name="running",
                tokens=("1730", "45:00", "gym", "5.2"),
                flags=["x"],
                options={
                    "avghr": "140",
                    "cal": "500",
                },
                comment=None,
            ),
        ),
        (
            "  running   1730   45:00   --avghr   140   ",
            RawUnit(
                name="running",
                tokens=("1730", "45:00"),
                flags=[],
                options={"avghr": "140"},
                comment=None,
            ),
        ),
        (
            "\trunning\t1730\t45:00\t-x",
            RawUnit(
                name="running",
                tokens=("1730", "45:00"),
                flags=["x"],
                options={},
                comment=None,
            ),
        ),
        (
            "running 1730 # --avghr 999 -x whatever",
            RawUnit(
                name="running",
                tokens=("1730",),
                flags=[],
                options={},
                comment="--avghr 999 -x whatever",
            ),
        ),
        (
            "running # # another # hash",
            RawUnit(
                name="running",
                tokens=(),
                flags=[],
                options={},
                comment="# another # hash",
            ),
        ),
    ],
)
def test_parse_line(line: str, expected: RawUnit) -> None:
    raw_unit = RawUnit.from_line(line)
    assert raw_unit == expected
