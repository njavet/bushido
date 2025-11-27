from typing import Any

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Collapsible, DataTable, ProgressBar


class LiftingScreen(Container):
    def compose(self) -> ComposeResult:
        with Collapsible(title="squat"):
            with Horizontal():
                yield DataTable(id="squat")
                yield ProgressBar(total=1.75, show_eta=False)
        with Collapsible(title="deadlift"):
            with Horizontal():
                yield DataTable(id="deadlift")
                yield ProgressBar(total=2, show_eta=False)
        with Collapsible(title="benchpress"):
            with Horizontal():
                yield DataTable(id="benchpress")
                yield ProgressBar(total=1.2, show_eta=False)

    def on_mount(self) -> None:
        dix: dict[str, Any] = {}

        table = self.query_one("#squat", DataTable)
        table.zebra_stripes = True
        table.add_columns(*dix["squat"][0])
        same = {}
        cc = 0
        for row in dix["squat"][1:]:
            if (row[0], row[1]) not in same:
                label = Text(str(cc))
                cc += 1
            else:
                label = Text("")
                same[row[0], row[1]] = 0
            table.add_row(*row, label=label)

        # table.add_rows(dix['squat'][1:])

        table = self.query_one("#deadlift", DataTable)
        table.add_columns(*dix["deadlift"][0])
        table.add_rows(dix["deadlift"][1:])

        table = self.query_one("#benchpress", DataTable)
        table.add_columns(*dix["benchpress"][0])
        table.add_rows(dix["benchpress"][1:])
