import datetime

import pytest

from bushido.units.base import ParsedUnit, Unit
from bushido.units.wimhof.db_model import WimhofRound, WimhofUnitTable
from bushido.units.wimhof.mapper import WimhofMapper
from bushido.units.wimhof.unit import RoundData, WimhofData


@pytest.fixture
def mapper() -> WimhofMapper:
    return WimhofMapper()


WIMHOF_CASES = [
    (
        ParsedUnit(
            name="wimhof",
            emoji="saturn",
            data=WimhofData(
                rounds=[
                    RoundData(round_nr=0, breaths=30, retention=90),
                    RoundData(round_nr=1, breaths=30, retention=120),
                    RoundData(round_nr=2, breaths=30, retention=150),
                ]
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        WimhofUnitTable(
            name="wimhof",
            emoji="saturn",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            rounds=[
                WimhofRound(round_nr=0, breaths=30, retention=90),
                WimhofRound(round_nr=1, breaths=30, retention=120),
                WimhofRound(round_nr=2, breaths=30, retention=150),
            ],
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, units", WIMHOF_CASES)
def test_correct_to_orm(
    mapper: WimhofMapper,
    parsed_unit: Unit[WimhofData],
    unit: WimhofUnitTable,
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, WimhofUnitTable)
    assert u.name == unit.name
    assert u.emoji == unit.emoji
    assert u.log_time == unit.log_time
    assert u.comment == unit.comment
    for i, rs in enumerate(u.rounds):
        assert isinstance(rs, WimhofRound)
        assert rs.round_nr == unit.rounds[i].round_nr
        assert rs.breaths == unit.rounds[i].breaths
        assert rs.retention == unit.rounds[i].retention


@pytest.mark.parametrize("parsed_unit, units", WIMHOF_CASES)
def test_correct_from_orm(
    mapper: WimhofMapper,
    parsed_unit: ParsedUnit[WimhofData],
    unit: WimhofUnitTable,
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, ParsedUnit)
    assert pu.emoji == unit.emoji
    assert pu.name == unit.name
    assert pu.log_time == unit.log_time
    assert pu.comment == unit.comment
    for i, rs in enumerate(pu.data.rounds):
        assert isinstance(rs, RoundData)
        assert rs.round_nr == unit.rounds[i].round_nr
        assert rs.breaths == unit.rounds[i].breaths
        assert rs.retention == unit.rounds[i].retention
