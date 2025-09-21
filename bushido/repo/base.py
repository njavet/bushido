from sqlalchemy.orm import Session

# project imports
from bushido.core.types import ORM_T


class UnitRepo:
    def __init__(self, session: Session):
        self.session = session

    # TODO handle exceptions
    def add(self, orm_lst: list[ORM_T]) -> bool:
        self.session.add_all(orm_lst)
        self.session.commit()
        return True
