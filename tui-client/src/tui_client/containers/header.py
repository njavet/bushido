from ..widgets.binary_clock import BinaryClock
from ..widgets.binary_date import BinaryDate
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual_image.widget import Image as ImageWidget


class HeaderContainer(Container):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield BinaryDate(id="bin_date")
            yield BinaryClock(id="bin_clock")
