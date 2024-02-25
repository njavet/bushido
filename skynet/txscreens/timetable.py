# general import*s
import datetime
from rich.table import Table
from textual.screen import ModalScreen
from textual.widgets import *
import config
from utils import utilities


class TimeTable(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, units):
        super().__init__()
        self.user_id = user_id
        self.units = units

    def collect_units(self):
        dix = {}
        for module_name in ['balance', 'wimhof', 'chrono', 'gym']:
            dtu = self.units[module_name].unit_retriever.date2unit_str(self.user_id)
            dix[module_name] = dtu
        return dix

    def compose(self):
        with TabbedContent(initial='tab-2024'):
            with TabPane('2020', id='tab-2020'):
                yield RichLog(id='log-2020')
            with TabPane('2021', id='tab-2021'):
                yield RichLog(id='log-2021')
            with TabPane('2022', id='tab-2022'):
                yield RichLog(id='log-2022')
            with TabPane('2023', id='tab-2023'):
                yield RichLog(id='log-2023')
            with TabPane('2024', id='tab-2024'):
                yield RichLog(id='log-2024')

    def on_mount(self):
        text_log = self.query_one('#log-2024', RichLog)
        dix = self.collect_units()
        table = construct_table(2024, dix)
        text_log.write(table)


def construct_table(year, dix):
    table = Table(title='Unit Timeline')
    table.add_column('Day')
    table.add_column('Date')
    table.add_column('Weight')
    table.add_column('Wimhof')
    table.add_column('Split')
    table.add_column('Gym')
    first = utilities.find_previous_sunday(
        datetime.date(year, 1, 1)
    )
    if datetime.datetime.now().year == year:
        last = utilities.find_next_saturday(
            datetime.date.today()
        )
    else:
        last = utilities.find_next_saturday(
            datetime.date(year, 12, 31)
        )

    days = (last - first).days
    while last >= first:
        dt = datetime.datetime.strftime(last, '%d.%m.%y')
        table.add_row(str(days),
                      dt,
                      dix['balance'][last],
                      dix['wimhof'][last],
                      dix['chrono'][last],
                      dix['gym'][last])
        if days % 7 == 0:
            table.add_section()
        last -= datetime.timedelta(days=1)
        days -= 1
    return table


