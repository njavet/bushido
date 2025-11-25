import datetime

from rich.table import Table
from textual.widget import Widget
from textual.widgets import Static


class BinaryClock(Widget):
    """4x6 binary clock widget."""

    def on_mount(self) -> None:
        self.set_interval(1.0, self.refresh, pause=False)

    def render(self) -> Table:
        now = datetime.datetime.now()
        # HHMMSS as 6 decimal digits
        digits = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
        on_char = "\u25a0"
        off_char = "\u25a1"

        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            collapse_padding=True,
        )

        # 6 columns (H_tens, H_units, M_tens, M_units, S_tens, S_units)
        for _ in range(6):
            table.add_column(justify="center", no_wrap=True)

        # 4 rows for 4 bits (MSB at top)
        for bit_row in range(3, -1, -1):  # 3,2,1,0
            cells: list[str] = []
            for ch in digits:
                d = int(ch)
                bit_on = (d >> bit_row) & 1
                cells.append(f"[cyan]{on_char}[/]" if bit_on else f"[dim]{off_char}[/]")
            table.add_row(*cells)

        return table


class Binclock(Static):
    def compose(self):
        for cell in range(24):
            yield Static("", classes="box", id="cell" + str(cell))

    def on_mount(self):
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        dt = datetime.datetime.now().strftime("%H%M%S")
        nums = [int(n) for n in dt]
        for i in range(6):
            for j, d in enumerate(bin(nums[i])[2:].zfill(4)):
                id_str = "#cell" + str(i + j * 6)
                cell = self.query_one(id_str, Static)
                cell.set_class(d == "1", "box-light")
