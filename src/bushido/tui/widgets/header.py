from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label
from textual_image.widget import Image as ImageWidget

from bushido.tui.widgets.binary_clock import BinaryClock
from bushido.tui.widgets.binary_date import BinaryDate


class HeaderContainer(Container):
    def __init__(
        self, belt: str, rank: str, belt_path: Path, rank_path: Path, id_: str
    ):
        super().__init__(id=id_)
        self.belt = belt
        self.rank = rank
        self.belt_path = belt_path
        self.rank_path = rank_path

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ImageWidget("src/bushido/static/bushido.png", id="bushido_img")
            yield BinaryDate(id="bin_date")
        with Vertical():
            yield Label("belt:")
            yield ImageWidget(str(self.belt_path), id="belt")
            yield Label(self.belt)
        with Vertical():
            yield Label("rank:")
            yield ImageWidget(str(self.rank_path), id="rank")
            yield Label(self.rank)
        with Horizontal():
            yield BinaryClock(id="bin_clock")
            yield ImageWidget("src/bushido/static/kyokushin.png", id="kyokushin_img")
