from textual.app import ComposeResult
from textual.containers import Container
from textual.coordinate import Coordinate
from textual.widgets import (
    DataTable,
    Markdown,
    TabbedContent,
    TabPane,
)

from bushido.categories.lifting import LiftingUnit


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent(id="lifting_tabs"):
            with TabPane("squat"):
                yield LiftingTable(id="squat_table")
            with TabPane("deadlift"):
                yield Markdown("TODO")
            with TabPane("benchpress"):
                yield Markdown("TODO")
            with TabPane("overheadpress"):
                yield Markdown("TODO")
            with TabPane("rows"):
                yield Markdown("TODO")

    def set_units(self, units: list[LiftingUnit]) -> None:
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

    def set_units(self, units: list[LiftingUnit]) -> None:
        self.clear()
        for unit in units:
            row_key = self.add_row(
                unit.log_time.strftime("%d.%m.%y"),
                "",
                "",
                "",
                "",
            )
            self.update_cell_at(
                Coordinate(row=int(row_key.value if row_key.value else 0), column=0),
                unit.log_time.strftime("%d.%m.%y"),
            )

            for lifting_set in unit.data.sets:
                self.add_row(
                    "",
                    str(lifting_set.set_nr),
                    str(lifting_set.weight),
                    str(lifting_set.reps),
                    str(lifting_set.rest),
                )
