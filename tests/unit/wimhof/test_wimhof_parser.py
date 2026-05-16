import pytest

from bushido.units.wimhof.parser import WimhofParser
from bushido.units.wimhof.unit import RoundData, WimhofData


@pytest.fixture
def parser() -> WimhofParser:
    return WimhofParser()


@pytest.mark.parametrize(
    "tokens, expected",
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
def test_correct_wimhof_unit(
    parser: WimhofParser, tokens: tuple[str, ...], expected: WimhofData
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
