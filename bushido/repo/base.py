from typing import TypeVar
from sqlalchemy.orm import Session


T = TypeVar('T')


class UnitRepo:
    def __init__(self, session: Session):
        self.session = session

    # TODO handle exceptions
    def add(self, orm_lst: list[T]) -> bool:
        self.session.add_all(orm_lst)
        self.session.commit()
        return True
