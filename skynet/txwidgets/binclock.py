import datetime
from textual.containers import Vertical
from textual.widgets import Digits, Static


class Binclock(Static):

    def compose(self):
        for cell in range(24):
            yield Static('', classes='box', id='cell' + str(cell))

    def on_mount(self):
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        dt = datetime.datetime.now().strftime('%H%M%S')
        nums = [int(n) for n in dt]
        for i in range(6):
            for j, d in enumerate(bin(nums[i])[2:].zfill(4)):
                id_str = '#cell' + str(i + j * 6)
                cell = self.query_one(id_str, Static)
                cell.set_class(d == '1', 'box-light')



