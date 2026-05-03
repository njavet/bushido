
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual_image.widget import Image as ImageWidget

from bushido.core.conf import BUSHIDO_IMG
from bushido.tui.widgets.binary_clock import BinaryClock
from bushido.tui.widgets.binary_date import BinaryDate


class HeaderContainer(Container):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield BinaryDate(id="bin_date")
            yield ImageWidget(BUSHIDO_IMG, id="bushido_img")
            yield BinaryClock(id="bin_clock")
