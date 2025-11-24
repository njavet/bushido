import datetime

from rich.table import Table
from textual.widget import Widget


class BinaryClock(Widget):
    """4x6 binary clock widget."""

    def on_mount(self) -> None:
        self.set_interval(1.0, self.refresh, pause=False)

    def render(self) -> Table:
        now = datetime.datetime.now()
        # HHMMSS as 6 decimal digits
        digits = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"

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
                cells.append("[green]●[/]" if bit_on else "[dim]·[/]")
            table.add_row(*cells)

        return table
