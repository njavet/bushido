import pytest

from bushidolib.units.wimhof import RoundData, WimhofData, parse_wimhof_unit


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (
            ("30", "90", "30", "120", "30", "150"),
            WimhofData(
                rounds=[
                    RoundData(round_nr=0, breaths=30, retention=90),
                    RoundData(round_nr=1, breaths=30, retention=120),
                    RoundData(round_nr=2, breaths=30, retention=150),
                ]
            ),
        ),
    ],
)
def test_correct_wimhof_unit(tokens: tuple[str, ...], expected: WimhofData) -> None:
    unit_data = parse_wimhof_unit(tokens)
    assert unit_data == expected
