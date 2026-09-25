import collections
from typing import override

from bushidolib.unit.martial_arts import MartialArtsUnit
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
)


class GymContainer(Container):
    def __init__(self, unit_settings: dict[str, str]) -> None:
        super().__init__()
        self.unit_settings = unit_settings

    @override
    def compose(self) -> ComposeResult:
        yield RichLog(id="gym_stats")
        yield GymTable(id="gym_table")

    def set_units(self, units: list[MartialArtsUnit]) -> None:
        self.query_one("#gym_table", GymTable).set_units(units)

    def add_unit(self, unit: MartialArtsUnit) -> None:
        self.log(unit)


class GymTable(DataTable[str]):
    @override
    def on_mount(self) -> None:
        self.add_columns("date", "training", "start", "end", "martial_arts")

    def set_units(self, units: list[MartialArtsUnit]) -> None:
        self.clear()
        by_day = collections.defaultdict(list)
        for unit in units:
            by_day[unit.log_time.date()].append(unit)

        for day, day_units in by_day.items():
            self.add_row(
                day.strftime("%d.%m.%y"),
                "",
                "",
                "",
                "",
            )

            for unit in day_units:
                self.add_row(
                    "",
                    " ".join([unit.kind]),
                    unit.start_t.strftime("%H%M"),
                    unit.end_t.strftime("%H%M"),
                    unit.gym,
                )
