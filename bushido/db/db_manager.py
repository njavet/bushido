from sqlalchemy import create_engine

# project imports
from bushido.db.models import Base


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)



class Uploader:
    def __init__(self):
        pass

    def init_tables(self, engine):
        Base.metadata.create_all(engine)


class Retriever:
    pass
