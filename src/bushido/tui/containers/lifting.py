from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
    TabbedContent,
    TabPane,
)

from bushido.units import Unit
from bushido.units.lifting import LiftingData, lifting_unit_settings


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent(id="lifting_tabs"):
            for unit_spec in lifting_unit_settings:
                with TabPane(" ".join([unit_spec.name, unit_spec.emoji])):
                    yield RichLog(id=f"{unit_spec.name}_stats")
                    yield LiftingTable(id=f"{unit_spec.name}_table")

    def set_units(self, units: list[Unit[LiftingData]]) -> None:
        for unit_spec in lifting_unit_settings:
            self.query_one(f"#{unit_spec.name}_table", LiftingTable).set_units(
                [u for u in units if u.name == unit_spec.name]
            )


class LiftingTable(DataTable[str]):
    def on_mount(self) -> None:
        self.add_columns("date", "set", "weight", "reps", "rest")

    def set_units(self, units: list[Unit[LiftingData]]) -> None:
        self.clear()
        for unit in units:
            self.add_row(
                unit.log_time.strftime("%d.%m.%y"),
                "",
                "",
                "",
                "",
            )

            for lifting_set in unit.data.sets:
                self.add_row(
                    "",
                    str(lifting_set.set_nr),
                    str(lifting_set.weight),
                    str(lifting_set.reps),
                    str(lifting_set.rest),
                )
