# general imports
import time

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Static


class StopwatchTimeDisplay(Static):
    """A widget to display elapsed time."""

    start_time = reactive(time.monotonic())
    seconds = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.seconds = self.total + (time.monotonic() - self.start_time)

    def watch_total(self, total):
        print(self.total)

    def watch_seconds(self, seconds: float) -> None:
        """Called when the time attribute changes."""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.update(f"{h:02,.0f}:{m:02.0f}:{s:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = time.monotonic()
        self.update_timer.resume()

    def pause(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += time.monotonic() - self.start_time
        self.seconds = self.total

    def end(self):
        self.seconds = 0
        self.total = 0


class Stopwatch(Container):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(StopwatchTimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
            self.query_one("#pause").disabled = False
        elif button_id == "pause":
            time_display.pause()
            self.add_class("paused")
        elif button_id == "resume":
            time_display.start()
            self.remove_class("paused")
        elif button_id == "end":
            time_display.pause()
            self.query_one("#pause").disabled = True
            self.remove_class("started")
            self.remove_class("paused")

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start")
        yield Button("Pause", disabled=True, id="pause")
        yield Button("Resume", id="resume")
        yield Button("End", id="end")
        yield StopwatchTimeDisplay()
