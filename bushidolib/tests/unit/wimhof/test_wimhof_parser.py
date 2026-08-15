import pytest

from bushidolib.wimhof import WimhofData, WimhofRoundData, parse_wimhof_unit


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (
            ("30", "90", "30", "120", "30", "150"),
            WimhofData(
                rounds=[
                    WimhofRoundData(round_nr=0, breaths=30, retention=90),
                    WimhofRoundData(round_nr=1, breaths=30, retention=120),
                    WimhofRoundData(round_nr=2, breaths=30, retention=150),
                ]
            ),
        ),
    ],
)
def test_correct_wimhof_unit(tokens: tuple[str, ...], expected: WimhofData) -> None:
    unit_data = parse_wimhof_unit(tokens)
    assert unit_data == expected
