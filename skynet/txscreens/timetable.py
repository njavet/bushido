# general import*s
import datetime
from rich.table import Table
from textual.screen import ModalScreen
from textual.widgets import *
import config
from utils import utilities


class TimeTable(ModalScreen):
    BINDINGS = [('b', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, unit_retrievers):
        super().__init__()
        self.user_id = user_id
        self.unit_retrievers = unit_retrievers

    def collect_units(self):
        for module_name in ['balance', 'wimhof']:
            dtu = self.unit_retrievers[module_name].date2units(self.user_id)


    def compose(self):
        with TabbedContent(initial='tab-2023'):
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
        text_log = self.query_one('#log-2023', RichLog)
        table = construct_table(2023)
        text_log.write(table)


def construct_table(year):
    table = Table(title='Unit Timeline')
    table.add_column('Day')
    table.add_column('Date')
    table.add_column('Weight')
    table.add_column('Wimhof')
    first = utilities.find_previous_sunday(
        datetime.datetime(year, 1, 1)
    )
    last = utilities.find_next_saturday(
        datetime.datetime.now()
    )

    days = (last - first).days
    while last >= first:
        dt = datetime.datetime.strftime(last, '%d.%m.%y')
        table.add_row(str(days), dt)
        if days % 7 == 0:
            table.add_section()
        last -= datetime.timedelta(days=1)
        days -= 1
    return table


