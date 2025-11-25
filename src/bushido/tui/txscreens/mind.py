import datetime
import time

# project imports
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Static


class Mind(Screen):
    def __init__(self, user_id, units):
        super().__init__()
        self.user_id = user_id
        self.units = units

    def compose(self) -> ComposeResult:
        pass

    def on_mount(self):
        for unit in self.units["study"]:
            pass


class Lecture(Container):
    tt = reactive(0)
    ttt = reactive(0)

    def __init__(self, lecture):
        super().__init__()
        self.lecture = lecture
        self.unit = mind.MindUnit(user_id=secconf.user_id, unit_name=lecture)

    def on_mount(self):
        today = datetime.datetime.today()
        query = StudyUnit.select().where(StudyUnit.name == self.lecture[0])
        self.tt = sum([q.minutes for q in query])
        query = [q for q in query if q.start.date() == today.date()]
        self.ttt = sum([q.minutes for q in query])

    def watch_tt(self, tt):
        m, s = divmod(tt, 60)
        h, m = divmod(m, 60)
        s0 = "Total Time Studied:\n"
        self.query_one("#time").update(s0 + f"{h:02,.0f}:{m:02.0f}:{s:02.0f}")

    def watch_ttt(self, ttt):
        m, s = divmod(ttt, 60)
        h, m = divmod(m, 60)
        s1 = "Today:\n"
        self.query_one("#today").update(s1 + f"{h:02,.0f}:{m:02.0f}:{s:02.0f}")

    def formatter(self):
        return " ".join([s.capitalize() for s in self.lecture[0].split("_")])

    def total_time(self):
        query = StudyUnit.select().where(StudyUnit.name == self.lecture[0])
        h, m = divmod(sum([q.minutes for q in query]), 60)
        s = 0
        s0 = "Total Time Studied:\n"
        return s0 + f"{h:02,.0f}:{m:02.0f}:{s:02.0f}"

    def today_time(self):
        today = datetime.datetime.today()
        query = StudyUnit.select().where(StudyUnit.name == self.lecture[0])
        query = [q for q in query if q.start.date() == today.date()]
        h, m = divmod(sum([q.minutes for q in query]), 60)
        s = 0
        s0 = "Today:\n"
        return s0 + f"{h:02,.0f}:{m:02.0f}:{s:02.0f}"

    def exam(self):
        s0 = "Exam Date:\n"
        s1 = datetime.datetime.strftime(self.lecture[1], "%H:%M - %d.%m.%y")
        return s0 + s1

    def compose(self):
        with Container():
            yield Title(self.formatter())
            yield Container(
                Exam(self.exam()),
                Body(self.total_time(), id="time"),
                Body(self.today_time(), id="today"),
            )
            yield Stopwatch()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        # time_display = self.query_one('StopwatchTimeDisplay')
        time_display = self.query_one("StopwatchTimeDisplay")
        if button_id == "start":
            self.unit.start = datetime.datetime.now()
            print("START seconds ", self.lecture[0], time_display.seconds)
            print("START total ", self.lecture[0], time_display.total)
        elif button_id == "pause":
            self.unit.breaks += 1
            print("PAUSE seconds ", self.lecture[0], time_display.seconds)
            print("PAUSE total ", self.lecture[0], time_display.total)
        elif button_id == "end":
            self.unit.end = datetime.datetime.now()
            self.unit.minutes = time_display.total // 60
            print("END seconds ", self.lecture[0], time_display.seconds)
            print("END total ", self.lecture[0], time_display.total)
            time_display.end()
            self.tt += self.unit.minutes
            self.ttt += self.unit.minutes
            self.unit.save()
            self.unit = StudyUnit(user=101, name=self.lecture[0])


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
