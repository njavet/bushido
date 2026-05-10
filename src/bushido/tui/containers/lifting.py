from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    Markdown,
    TabbedContent,
    TabPane,
)

from bushido.categories.lifting import LiftingUnit


class LiftingContainer(Container):
    def compose(self) -> ComposeResult:
        with TabbedContent():
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
        self.query_one(LiftingTable).set_units(units)


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

            self.update_cell_at((row_key, 0), unit.log_time.strftime("%d.%m.%y"))

            for lifting_set in unit.data.sets:
                self.add_row(
                    str(lifting_set.set_nr),
                    str(lifting_set.weight),
                    str(lifting_set.reps),
                    str(lifting_set.rest),
                )
