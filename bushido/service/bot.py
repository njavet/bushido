
# project imports
from bushido.data.conn import SessionFactory


class Bot:
    def __init__(self):
        self.sf =  SessionFactory()
