
from rich.text import Text
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Collapsible, DataTable, ProgressBar


class LiftingScreen(ModalScreen):
    BINDINGS = [("q", "app.pop_screen", "Back")]

    def __init__(self, user_id, umodules):
        super().__init__()
        self.user_id = user_id
        self.umodules = umodules

    def compose(self):
        with Collapsible(title="Squat"):
            with Horizontal():
                yield DataTable(id="squat")
                yield ProgressBar(total=1.75, show_eta=False)
        with Collapsible(title="Deadlift"):
            with Horizontal():
                yield DataTable(id="deadlift")
                yield ProgressBar(total=2, show_eta=False)
        with Collapsible(title="Benchpress"):
            with Horizontal():
                yield DataTable(id="benchpress")
                yield ProgressBar(total=1.2, show_eta=False)

    def on_mount(self):
        dix = self.umodules["lifting"].unit_name2unit_list(self.user_id)

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
                label = ""
                same[row[0], row[1]] = 0
            table.add_row(*row, label=label)

        # table.add_rows(dix['squat'][1:])

        table = self.query_one("#deadlift", DataTable)
        table.add_columns(*dix["deadlift"][0])
        table.add_rows(dix["deadlift"][1:])

        table = self.query_one("#benchpress", DataTable)
        table.add_columns(*dix["benchpress"][0])
        table.add_rows(dix["benchpress"][1:])
