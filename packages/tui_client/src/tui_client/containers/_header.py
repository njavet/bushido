from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual_image.widget import Image as ImageWidget

from tui_client.settings import BUSHIDO_IMG_PATH
from tui_client.widgets.binary_clock import BinaryClock
from tui_client.widgets.binary_date import BinaryDate


class HeaderContainer(Container):
    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield BinaryDate(id="bin_date")
            yield ImageWidget(BUSHIDO_IMG_PATH, id="bushido_img")
            yield BinaryClock(id="bin_clock")
