from dataclasses import dataclass

from bushido.units.exceptions import ParsingError

from .unit import RoundData, WimhofData


@dataclass(frozen=True, slots=True)
class WimhofParser:
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> WimhofData:
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

        return WimhofData(
            rounds=[
                RoundData(round_nr=i, breaths=b, retention=r)
                for i, (b, r) in enumerate(zip(breaths, retentions))
            ]
        )
