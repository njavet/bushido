import datetime

from rich.table import Table
from textual.widget import Widget


class BinaryDate(Widget):
    """4x6 binary date widget."""

    def on_mount(self) -> None:
        # TODO determine update interval
        self.set_interval(1.0, self.refresh, pause=False)

    def render(self) -> Table:
        today = datetime.date.today()
        digits = datetime.datetime.strftime(today, "%d%m%y")
        on_char = "\u25a0"
        off_char = "\u25a1"

        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            collapse_padding=True,
        )

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
