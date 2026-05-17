import collections

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
)

from bushido.units import Unit
from bushido.units.gym import GymData


class GymContainer(Container):
    def compose(self) -> ComposeResult:
        yield RichLog(id="gym_stats")
        yield GymTable(id="gym_table")

    def set_units(self, units: list[Unit[GymData]]) -> None:
        self.query_one("#gym_table", GymTable).set_units(units)


class GymTable(DataTable[str]):
    def on_mount(self) -> None:
        self.add_columns("date", "training", "start", "end", "gym")

    def set_units(self, units: list[Unit[GymData]]) -> None:
        self.clear()
        by_day = collections.defaultdict(list)
        for unit in units:
            by_day[unit.log_time.date()].append(unit)

        for day, units in by_day.items():
            self.add_row(
                day.strftime("%d.%m.%y"),
                "",
                "",
                "",
                "",
            )

            for unit in units:
                self.add_row(
                    "",
                    str(unit.name),
                    unit.start_t.strftime("%H%M"),
                    unit.end_t.strftime("%H%M"),
                    unit.gym,
                )
