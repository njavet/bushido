from dataclasses import dataclass

from ..exceptions import ParsingError
from .spec import Data, RoundData


@dataclass(frozen=True, slots=True)
class Parser:
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Data:
        breaths = [int(b) for b in tokens[::2]]
        retentions = [int(r) for r in tokens[1::2]]
        if len(breaths) == 0:
            raise ParsingError("at least one round")
        if len(breaths) != len(retentions):
            raise ParsingError(f"breaths and retentions don't match {tokens}")
        if any(x < 0 for x in breaths):
            raise ParsingError("breaths must all be positive")
        if any(x < 0 for x in retentions):
            raise ParsingError("retentions must all be positive")

        return Data(
            rounds=[
                RoundData(round_nr=i, breaths=b, retention=r)
                for i, (b, r) in enumerate(zip(breaths, retentions))
            ]
        )
