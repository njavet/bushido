import pytest

from bushido.units.wimhof.parser import Parser
from bushido.units.wimhof.unit import Data, RoundData


@pytest.fixture
def parser() -> Parser:
    return Parser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("30", "90", "30", "120", "30", "150"),
            Data(
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
    parser: Parser, tokens: tuple[str, ...], expected: Data
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
