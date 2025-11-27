from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, ProgressBar
from textual_image.widget import Image as ImageWidget

from bushido.core.conf import BUSHIDO_IMG, KYOKUSHIN_IMG
from bushido.tui.widgets.binary_clock import BinaryClock
from bushido.tui.widgets.binary_date import BinaryDate


class HeaderContainer(Container):
    def __init__(self, rank: str, rank_path: Path, id_: str):
        super().__init__(id=id_)
        self.rank = rank
        self.rank_path = rank_path

    # TODO proper alignment
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ImageWidget(BUSHIDO_IMG, id="bushido_img")
            yield BinaryDate(id="bin_date")
        with Vertical():
            yield Label("rank:")
            yield ImageWidget(str(self.rank_path), id="rank")
            yield Label(self.rank)
        with Vertical():
            yield ProgressBar(id="progress")
        with Horizontal():
            yield BinaryClock(id="bin_clock")
            yield ImageWidget(KYOKUSHIN_IMG, id="kyokushin_img")
