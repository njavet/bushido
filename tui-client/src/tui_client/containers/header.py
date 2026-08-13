from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Horizontal

from ..widgets.binary_clock import BinaryClock
from ..widgets.binary_date import BinaryDate


class HeaderContainer(Container):
    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield BinaryDate(id="bin_date")
            yield BinaryClock(id="bin_clock")
