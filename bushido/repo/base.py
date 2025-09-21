from abc import ABC, abstractmethod
from typing import Generic
from sqlalchemy.orm import Session

# project imports
from bushido.core.types import ORM_T, ORM_ST


class UnitRepo(Generic[ORM_T, ORM_ST], ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def add_unit(self, unit: ORM_T, subunits: list[ORM_ST]) -> bool:
        ...
