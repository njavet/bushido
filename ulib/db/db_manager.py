from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import pandas as pd

# project imports
from .models import Base, Emoji, Category
from .retriever import Retriever
from .uploader import Uploader


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.retriever = Retriever(self.engine)
        self.uploader = Uploader(self.engine)

    def init_db(self):
        self.init_tables()
        self.uploader.upload_category_data()
        self.uploader.upload_emoji_data()

    def init_tables(self, tables=None):
        if tables is not None:
            tables = [table.__table__ for table in tables]
            Base.metadata.create_all(self.engine, tables=tables)
        else:
            Base.metadata.create_all(self.engine)

    def drop_tables(self, tables=None):
        if tables is not None:
            tables = [table.__table__ for table in tables]
            Base.metadata.drop_all(self.engine, tables=tables)
        else:
            Base.metadata.drop_all(self.engine)
