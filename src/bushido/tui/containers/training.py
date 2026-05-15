from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    Markdown,
    TabbedContent,
    TabPane,
)

from bushido.category.dtypes import TrainingUnit


class TrainingTable(DataTable[str]):
    def on_mount(self) -> None:
        self.add_columns(
            "emoji", "date", "start", "end", "time", "training", "gym", "comment"
        )

    def set_units(self, units: list[TrainingUnit]) -> None:
        self.clear()
        for unit in units:
            self.add_row(
                unit.emoji,
                unit.date.strftime("%d.%m.%y"),
                unit.start_t.strftime("%H%M") if unit.start_t else "",
                unit.end_t.strftime("%H%M") if unit.end_t else "",
                str(unit.duration),
                unit.name,
                unit.gym if unit.gym else "",
                unit.comment if unit.comment else "",
            )


class GymContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent(id="gym_tabs"):
            with TabPane("table"):
                yield TrainingTable(id="training_table")
            with TabPane("stats"):
                yield Markdown("TODO")

    def set_units(self, units: list[TrainingUnit]) -> None:
        self.query_one(TrainingTable).set_units(units)
