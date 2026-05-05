from collections import defaultdict
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    TabbedContent,
    TabPane,
)

from bushido.categories.dtypes import ParsedUnit
from bushido.categories.gym.parser import GymSpec


class TrainingTable(DataTable[Any]):
    def on_mount(self) -> None:
        self.add_columns("Date", "Time", "Training", "Gym", "Comment")

    def set_units(self, units: list[ParsedUnit[GymSpec]]) -> None:
        self.clear()
        for unit in units:
            self.add_row(
                unit.log_time,
                unit.data.start_t,
                unit.name,
                unit.data.location,
                unit.comment,
            )


class GymContainer(Container):
    def __init__(self, units: list[ParsedUnit[GymSpec]]) -> None:
        super().__init__()
        self.units = units

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("MartialArts"):
                yield TrainingTable(id="martial_arts_table")
            with TabPane("Weights"):
                yield TrainingTable(id="weights_table")

    async def on_mount(self) -> None:

        by_category = defaultdict(list)
        for unit in self.units:
            by_category[unit.name].append(unit)

        for t, u in by_category.items():
            table = self.query_one(f"#{t}_table", TrainingTable)
            table.set_units(u)
