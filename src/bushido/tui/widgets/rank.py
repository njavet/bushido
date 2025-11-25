from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual_image.widget import Image as ImageWidget


class RankWidget(Static):
    def __init__(self, title: str, content: str, image_path: Path):
        super().__init__()
        self.title = title
        self.content = content
        self.image_path = image_path

    def compose(self) -> ComposeResult:
        yield Label(self.title)
        yield ImageWidget(str(self.image_path))
        yield Label(self.content)
