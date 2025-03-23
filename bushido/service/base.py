
# project imports
from bushido.data.base import DatabaseManager
from bushido.service.categories.category import InputProcessor


class BaseService:
    def __init__(self):
        self.dbm = DatabaseManager(db_url='sqlite:///bushido.db')
        self.iproc = InputProcessor()

