from sqlalchemy.orm import Session

from bushido.units.repo import UnitRepo

from .db_model import MartialArtsUnitTable


class MartialArtsRepo(UnitRepo[MartialArtsUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, MartialArtsUnitTable)
