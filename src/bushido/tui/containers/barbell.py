from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
    TabbedContent,
    TabPane,
)

from bushido.units.base import Unit
from bushido.units.lifting.unit import BarbellData


class BarbellContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent(id="lifting_tabs"):
            with TabPane("squat"):
                yield RichLog(id="squat_stats")
                yield BarbellTable(id="squat_table")
            with TabPane("deadlift"):
                yield BarbellTable(id="deadlift_table")
            with TabPane("benchpress"):
                yield BarbellTable(id="benchpress_table")
            with TabPane("overheadpress"):
                yield BarbellTable(id="overheadpress_table")
            with TabPane("rows"):
                yield BarbellTable(id="rows_table")

    def set_units(self, units: list[Unit[BarbellData]]) -> None:
        self.query_one("#squat_table", BarbellTable).set_units(
            [u for u in units if u.name == "squat"]
        )
        self.query_one("#deadlift_table", BarbellTable).set_units(
            [u for u in units if u.name == "deadlift"]
        )
        self.query_one("#benchpress_table", BarbellTable).set_units(
            [u for u in units if u.name == "benchpress"]
        )
        self.query_one("#overheadpress_table", BarbellTable).set_units(
            [u for u in units if u.name == "overheadpress"]
        )
        self.query_one("#rows_table", BarbellTable).set_units(
            [u for u in units if u.name == "rows"]
        )


class BarbellTable(DataTable[str]):
    def on_mount(self) -> None:
        self.add_columns("date", "set", "weight", "reps", "rest")

    def set_units(self, units: list[Unit[BarbellData]]) -> None:
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
