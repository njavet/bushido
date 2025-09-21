from pydantic import BaseModel

from bushido.domain.unit import UnitSpec


class UnitLogRequest(BaseModel):
    words: list[str]
    comment: str | None = None

    def to_spec(self, unit_name: str):
        return UnitSpec(unit_name=unit_name, words=self.words, comment=self.comment)
