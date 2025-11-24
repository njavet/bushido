from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Static
from textual_image.widget import Image as ImageWidget


class BeltCard(Vertical):
    def __init__(self, belt_name: str, image_path: Path) -> None:
        super().__init__()
        self.belt_name = belt_name
        self.image_path = image_path

    def compose(self) -> ComposeResult:
        yield ImageWidget(str(self.image_path))
        yield Static(self.belt_name, classes="belt-name")

        yield Static("Bushido Admin Panel", id="header")
        yield Horizontal(
            BeltCard("White Belt", Path("black_belt.png")),
            id="belt-row",
        )
        yield Footer()
