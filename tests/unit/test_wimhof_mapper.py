import datetime

import pytest
from bushido.category.dtypes import ParsedUnit
from bushido.category.wimhof.domain import RoundSpec, WimhofSpec, WimhofUnit
from bushido.category.wimhof.mapper import WimhofMapper
from bushido.category.wimhof.orm import WimhofRound, WimhofUnitTable


@pytest.fixture
def mapper() -> WimhofMapper:
    return WimhofMapper()


WIMHOF_CASES = [
    (
        ParsedUnit(
            name="wimhof",
            emoji="saturn",
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
        WimhofUnitTable(
            name="wimhof",
            emoji="saturn",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            subunits=[
                WimhofRound(round_nr=0, breaths=30, retention=90),
                WimhofRound(round_nr=1, breaths=30, retention=120),
                WimhofRound(round_nr=2, breaths=30, retention=150),
            ],
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, unit", WIMHOF_CASES)
def test_correct_to_orm(
    mapper: WimhofMapper,
    parsed_unit: WimhofUnit,
    unit: WimhofUnitTable,
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, WimhofUnitTable)
    assert u.name == unit.name
    assert u.emoji == unit.emoji
    assert u.log_time == unit.log_time
    assert u.comment == unit.comment
    for i, rs in enumerate(u.subunits):
        assert isinstance(rs, WimhofRound)
        assert rs.round_nr == unit.subunits[i].round_nr
        assert rs.breaths == unit.subunits[i].breaths
        assert rs.retention == unit.subunits[i].retention


@pytest.mark.parametrize("parsed_unit, unit", WIMHOF_CASES)
def test_correct_from_orm(
    mapper: WimhofMapper,
    parsed_unit: ParsedUnit[WimhofSpec],
    unit: WimhofUnitTable,
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, ParsedUnit)
    assert pu.emoji == unit.emoji
    assert pu.name == unit.name
    assert pu.log_time == unit.log_time
    assert pu.comment == unit.comment
    for i, rs in enumerate(pu.data.rounds):
        assert isinstance(rs, RoundSpec)
        assert rs.round_nr == unit.subunits[i].round_nr
        assert rs.breaths == unit.subunits[i].breaths
        assert rs.retention == unit.subunits[i].retention
