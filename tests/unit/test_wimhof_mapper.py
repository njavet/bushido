import datetime

import pytest

from bushido.units.parsing.base import ParsedUnit
from bushido.units.wimhof import (
    WimhofMapper,
    WimhofRound,
    WimhofUnit,
)
from bushido.units.wimhof.parser import RoundSpec, WimhofSpec


@pytest.fixture
def mapper() -> WimhofMapper:
    return WimhofMapper()


WIMHOF_CASES = [
    (
        ParsedUnit(
            name="wimhof",
            data=WimhofSpec(
                rounds=[
                    RoundSpec(round_nr=0, breaths=30, retention=90),
                    RoundSpec(round_nr=1, breaths=30, retention=120),
                    RoundSpec(round_nr=2, breaths=30, retention=150),
                ]
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        WimhofUnit(
            name="wimhof",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
        ),
        [
            WimhofRound(round_nr=0, breaths=30, retention=90),
            WimhofRound(round_nr=1, breaths=30, retention=120),
            WimhofRound(round_nr=2, breaths=30, retention=150),
        ],
    ),
]


@pytest.mark.parametrize("parsed_unit, unit, rounds", WIMHOF_CASES)
def test_correct_to_orm(
    mapper: WimhofMapper,
    parsed_unit: ParsedUnit[WimhofSpec],
    unit: WimhofUnit,
    rounds: list[WimhofRound],
) -> None:
    u, r = mapper.to_orm(parsed_unit)
    assert isinstance(u, WimhofUnit)
    assert u.name == unit.name
    assert u.log_time == unit.log_time
    assert u.comment == unit.comment
    for i, rs in enumerate(r):
        assert isinstance(rs, WimhofRound)
        assert rs.round_nr == rounds[i].round_nr
        assert rs.breaths == rounds[i].breaths
        assert rs.retention == rounds[i].retention


@pytest.mark.parametrize("parsed_unit, unit, rounds", WIMHOF_CASES)
def test_correct_from_orm(
    mapper: WimhofMapper,
    parsed_unit: ParsedUnit[WimhofSpec],
    unit: WimhofUnit,
    rounds: list[WimhofRound],
) -> None:
    pu = mapper.from_orm((unit, rounds))
    assert isinstance(pu, ParsedUnit)
    assert pu.name == unit.name
    assert pu.log_time == unit.log_time
    assert pu.comment == unit.comment
    for i, rs in enumerate(pu.data.rounds):
        assert isinstance(rs, RoundSpec)
        assert rs.round_nr == rounds[i].round_nr
        assert rs.breaths == rounds[i].breaths
        assert rs.retention == rounds[i].retention
