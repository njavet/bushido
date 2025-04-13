
# project imports
from bushido.conf import DB_URL
from bushido.data.manager import DataManager
from bushido.service.units import UnitProcessor


def setup_dm():
    dm = DataManager(db_url=DB_URL)
    return dm


def setup_up(dm):
    up = UnitProcessor(dm)
    return up
