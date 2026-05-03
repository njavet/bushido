import pytest

from bushido.core.result import Ok
from bushido.units.wimhof import RoundSpec, WimhofParser, WimhofSpec


@pytest.fixture
def parser() -> WimhofParser:
    return WimhofParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("30", "90", "30", "120", "30", "150"),
            WimhofSpec(
                rounds=[
                    RoundSpec(round_nr=0, breaths=30, retention=90),
                    RoundSpec(round_nr=1, breaths=30, retention=120),
                    RoundSpec(round_nr=2, breaths=30, retention=150),
                ]
            ),
        ),
    ],
)
def test_correct_wimhof_unit(
    parser: WimhofParser, tokens: tuple[str, ...], expected: WimhofSpec
) -> None:
    result = parser.parse(tokens)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected
