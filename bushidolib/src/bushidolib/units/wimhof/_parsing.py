from bushidolib.exceptions import UnitParsingError

from ._spec import WimhofData, WimhofRoundData


def parse(tokens: tuple[str, ...]) -> WimhofData:
    breaths = [int(b) for b in tokens[::2]]
    retentions = [int(r) for r in tokens[1::2]]
    if len(breaths) == 0:
        raise UnitParsingError("at least one round")
    if len(breaths) != len(retentions):
        raise UnitParsingError(f"breaths and retentions don't match {tokens}")
    if any(x < 0 for x in breaths):
        raise UnitParsingError("breaths must all be positive")
    if any(x < 0 for x in retentions):
        raise UnitParsingError("retentions must all be positive")

    return WimhofData(
        rounds=[
            WimhofRoundData(round_nr=i, breaths=b, retention=r)
            for i, (b, r) in enumerate(zip(breaths, retentions, strict=False))
        ]
    )
