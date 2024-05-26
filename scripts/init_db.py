
from unit_manager import UnitManager
from dotenv import load_dotenv
import db
import config
import pytz
import datetime
import os


if __name__ == '__main__':
    load_dotenv()
    agent_id = int(os.getenv('AGENT_ID'))
    to_id = int(os.getenv('T800_ID'))

    um = UnitManager(config.emojis)
    models = [u.subunit_model for u in um.unit_modules.values()]
    db.init_storage(models)

    db.add_agent(agent_id, 'N300', True)

    utc = pytz.timezone('utc')
    dt0 = datetime.datetime(2024, 5, 26, 9, 10).astimezone(utc)
    s0 = '⚖️  94.6 18 59.8 39.1'
    t0 = dt0.timestamp()

    um.process_string(s0)
    um.save_unit_data(agent_id, to_id, t0)


    s1 = '⛩ 80 5 180 80 5 180 80 5'
    dt1 = datetime.datetime(2024, 5, 26, 10, 45).astimezone(utc)
    t1 = dt1.timestamp()
    um.process_string(s1)
    um.save_unit_data(agent_id, to_id, t1)

    s2 = '🦍 1030-1100 hm'
    dt2 = datetime.datetime(2024, 5, 26, 11, 7, 4).astimezone(utc)
    t2 = dt2.timestamp()
    um.process_string(s2)
    um.save_unit_data(agent_id, to_id, t2)

