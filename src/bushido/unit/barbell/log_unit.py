from sqlalchemy.orm import Session

from ...core.exceptions import ParsingError
from ..base import Unit, UnitLogRequest
from .mapper import BarbellMapper
from .parser import BarbellParser
from .repo import BarbellRepo


class LogUnit:
    def __init__(self) -> None:
        self.parser = BarbellParser()
        self.mapper = BarbellMapper()

    def log_unit(self, req: UnitLogRequest, session: Session) -> str:
        try:
            unit_data = self.parser.parse(req.tokens)
        except ParsingError as e:
            return str(e)

        parsed_unit = Unit(
            name=req.name,
            emoji="",
            data=unit_data,
            log_time=req.log_time,
            comment=req.comment,
        )
        unit = self.mapper.to_orm(parsed_unit)
        BarbellRepo(session).add_unit(unit)
        return "confirmed"
