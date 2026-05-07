from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    Markdown,
    TabbedContent,
    TabPane,
)

from bushido.categories.gym import GymUnit


class TrainingTable(DataTable[Any]):
    def on_mount(self) -> None:
        self.add_columns("date", "time", "training", "gym", "comment")

    def set_units(self, units: list[GymUnit]) -> None:
        self.clear()
        for unit in units:
            self.add_row(
                unit.log_time,
                unit.data.start_t,
                unit.name,
                unit.data.gym,
                unit.comment,
            )


class GymContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("stats"):
                yield Markdown("TODO")
            with TabPane("table"):
                yield TrainingTable(id="training_table")

    def set_units(self, units: list[GymUnit]) -> None:
        self.query_one(TrainingTable).set_units(units)
