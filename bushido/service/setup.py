
# project imports
from bushido.data.manager import DataManager


def setup_dm(db_url):
    dm = DataManager(db_url)
    return dm
