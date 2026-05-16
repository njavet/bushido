from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
    TabbedContent,
    TabPane,
)

from bushido.units.base import Unit
from bushido.units.lifting.unit import Data


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent(id="lifting_tabs"):
            with TabPane("squat"):
                yield RichLog(id="squat_stats")
                yield LiftingTable(id="squat_table")
            with TabPane("deadlift"):
                yield LiftingTable(id="deadlift_table")
            with TabPane("benchpress"):
                yield LiftingTable(id="benchpress_table")
            with TabPane("overheadpress"):
                yield LiftingTable(id="overheadpress_table")
            with TabPane("rows"):
                yield LiftingTable(id="rows_table")

    def set_units(self, units: list[Unit[Data]]) -> None:
        self.query_one("#squat_table", LiftingTable).set_units(
            [u for u in units if u.name == "squat"]
        )
        self.query_one("#deadlift_table", LiftingTable).set_units(
            [u for u in units if u.name == "deadlift"]
        )
        self.query_one("#benchpress_table", LiftingTable).set_units(
            [u for u in units if u.name == "benchpress"]
        )
        self.query_one("#overheadpress_table", LiftingTable).set_units(
            [u for u in units if u.name == "overheadpress"]
        )
        self.query_one("#rows_table", LiftingTable).set_units(
            [u for u in units if u.name == "rows"]
        )


class LiftingTable(DataTable[str]):
    def on_mount(self) -> None:
        self.add_columns("date", "set", "weight", "reps", "rest")

    def set_units(self, units: list[Unit[Data]]) -> None:
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
