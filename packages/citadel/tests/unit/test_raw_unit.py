import pytest

from citadel.bcl import LogUnitCommand, log_parser
from citadel.bcl.errors import CommandSyntaxError


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "some-unit",
            LogUnitCommand(
                unit_name="some-unit",
                args=(),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "running 1730",
            LogUnitCommand(
                unit_name="running",
                args=("1730",),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "athena 1730 45:00 gym 5.2",
            LogUnitCommand(
                unit_name="athena",
                args=("1730", "45:00", "gym", "5.2"),
                flags=[],
                options={},
                comment=None,
            ),
        ),
        (
            "platon -x",
            LogUnitCommand(
                unit_name="platon",
                args=(),
                flags=["x"],
                options={},
                comment=None,
            ),
        ),
        (
            "kant -x -y -z",
            LogUnitCommand(
                unit_name="kant",
                args=(),
                flags=["x", "y", "z"],
                options={},
                comment=None,
            ),
        ),
        (
            "starcraft --avghr 140",
            LogUnitCommand(
                unit_name="starcraft",
                args=(),
                flags=[],
                options={"avghr": "140"},
                comment=None,
            ),
        ),
        (
            "jogging --avghr 140 --maxhr 175 --cal 500",
            LogUnitCommand(
                unit_name="jogging",
                args=(),
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
            LogUnitCommand(
                unit_name="running",
                args=(),
                flags=[],
                options={},
                comment="easy run",
            ),
        ),
        (
            "running 1730 45:00 # easy zone 2 run",
            LogUnitCommand(
                unit_name="running",
                args=("1730", "45:00"),
                flags=[],
                options={},
                comment="easy zone 2 run",
            ),
        ),
        (
            "running 1730 45:00 gym 16.4 -x --avghr 160 --maxhr 187 --cal 500 # hard",
            LogUnitCommand(
                unit_name="running",
                args=("1730", "45:00", "gym", "16.4"),
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
            LogUnitCommand(
                unit_name="running",
                args=("1730", "45:00", "gym", "5.2"),
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
            LogUnitCommand(
                unit_name="running",
                args=("1730", "45:00"),
                flags=[],
                options={"avghr": "140"},
                comment=None,
            ),
        ),
        (
            "\trunning\t1730\t45:00\t-x",
            LogUnitCommand(
                unit_name="running",
                args=("1730", "45:00"),
                flags=["x"],
                options={},
                comment=None,
            ),
        ),
        (
            "running 1730 # --avghr 999 -x whatever",
            LogUnitCommand(
                unit_name="running",
                args=("1730",),
                flags=[],
                options={},
                comment="--avghr 999 -x whatever",
            ),
        ),
        (
            "running # # another # hash",
            LogUnitCommand(
                unit_name="running",
                args=(),
                flags=[],
                options={},
                comment="# another # hash",
            ),
        ),
        (
            "poseidon --tmp -5 # # another # hash",
            LogUnitCommand(
                unit_name="poseidon",
                args=(),
                flags=[],
                options={"tmp": "-5"},
                comment="# another # hash",
            ),
        ),
    ],
)
def test_parse_line(line: str, expected: LogUnitCommand) -> None:
    cmd = log_parser(line)
    assert cmd == expected


@pytest.mark.parametrize(
    "line",
    [
        "",
        "   ",
        "\t",
        "--avghr=140",  # no unit unit_name
        "-x",  # no unit unit_name
        "# comment only",  # no unit unit_name
        # Important ambiguity:
        "swimming --avghr=140 --avghr=150",
    ],
)
def test_parse_line_rejects_invalid_syntax(line: str) -> None:
    with pytest.raises(CommandSyntaxError):
        _ = log_parser(line)
