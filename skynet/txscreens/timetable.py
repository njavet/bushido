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
    start = utilities.find_previous_sunday(
        datetime.datetime(year, 1, 1))
    while start <= datetime.datetime(year, 12, 31):
        dt = datetime.datetime.strftime(start, '%d.%m.%y')
        table.add_row(dt)
        start += datetime.timedelta(days=1)
    return table


