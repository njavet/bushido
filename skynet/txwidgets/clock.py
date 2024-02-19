import datetime
from textual.widgets import Digits, Static


class Clock(Static):

    def compose(self):
        yield Digits('', id='clock')

    def on_mount(self):
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        dt = datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%y %H:%M:%S')
        self.query_one(Digits).update(dt)
