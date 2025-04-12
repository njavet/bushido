from sqlalchemy import create_engine

# project imports


class DataManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)

