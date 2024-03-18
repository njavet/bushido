# general import*s
import collections
import datetime
import peewee as pw
from rich.table import Table
from textual.screen import ModalScreen
from textual.widgets import *
import config
from utils import utilities

from db import Unit
from units.balance import Balance
from units.wimhof import Wimhof
from units.chrono import Chrono
from units.gym import Gym
from units.lifting import Lifting


class TimeTable(ModalScreen):
    BINDINGS = [('q', 'app.pop_screen', 'Back')]

    def __init__(self, user_id, modules):
        super().__init__()
        self.user_id = user_id
        self.modules = modules

    def collect_units(self):
        sq0 = (Unit
               .select(Unit.log_date, Unit.unit_emoji, Balance.weight)
               .join(Balance)
               .group_by(Unit.log_date)
               .alias('balance_units')
               )

        sq1 = (Unit
               .select(Unit.log_date, Unit.unit_emoji)
               .join(Wimhof)
               .group_by(Unit.log_date)
               .alias('wimhof_units')
               )

        sq2 = (Unit
               .select(Unit.log_date, Unit.unit_emoji)
               .join(Chrono)
               .group_by(Unit.log_date)
               .alias('chrono_units')
               )

        q0 = (Unit
              .select(Unit,
                      sq0.c.weight.alias('bw'),
                      sq0.c.unit_emoji.alias('bu_emoji'),
                      sq1.c.unit_emoji.alias('wu_emoji'),
                      sq2.c.unit_emoji.alias('cu_emoij'))
              .join(Gym, pw.JOIN.LEFT_OUTER)
              .switch(Unit)
              .join(sq0, pw.JOIN.LEFT_OUTER, on=(Unit.log_date == sq0.c.log_date))
              .switch(Unit)
              .join(sq1, pw.JOIN.LEFT_OUTER, on=(Unit.log_date == sq1.c.log_date))
              .switch(Unit)
              .join(sq2, pw.JOIN.LEFT_OUTER, on=(Unit.log_date == sq2.c.log_date))
              .order_by(Unit.log_time.desc())
              )

        return q0
        dix = {}
        for module_name in ['balance', 'wimhof', 'chrono', 'gym']:
            dtu = self.modules[module_name].date2unit_str(self.user_id)
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
    dd = collections.defaultdict(list)
    for q in dix:
        dd[q.log_date].append(q)

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
                      str(dd[last]))

        """
        table.add_row(str(days),
                      dt,
                      dix['balance'][last],
                      dix['wimhof'][last],
                      dix['chrono'][last],
                      dix['gym'][last])
                      """
        if days % 7 == 0:

            table.add_section()
        last -= datetime.timedelta(days=1)
        days -= 1
    return table


