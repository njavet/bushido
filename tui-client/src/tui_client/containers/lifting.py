# TODO api
from typing import override

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    RichLog,
    TabbedContent,
    TabPane,
)

from bushidolib.contracts.unit import LiftingUnit
from tui_client.settings import UnitConf


class LiftingContainer(Container):
    def __init__(self, unit_settings: dict[str, UnitConf]) -> None:
        super().__init__()
        self.unit_settings = unit_settings

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent(id="lifting_tabs"):
            for name, uc in self.unit_settings.items():
                with TabPane(" ".join([name, uc.emoji])):
                    yield RichLog(id=f"{name}_stats")
                    yield LiftingTable(id=f"{name}_table")

    def set_units(self, units: list[LiftingUnit]) -> None:
        for unit_spec in units:
            self.query_one(f"#{unit_spec.name}_table", LiftingTable).set_units(
                [u for u in units if u.name == unit_spec.name]
            )


class LiftingTable(DataTable[str]):
    @override
    def on_mount(self) -> None:
        self.add_columns("date", "set", "weight", "reps", "rest")

    def set_units(self, units: list[LiftingUnit]) -> None:
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
