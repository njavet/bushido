from bushidolib.exceptions import ParsingUnitError

from ._spec import RoundData, WimhofData


def parse(tokens: tuple[str, ...]) -> WimhofData:
    breaths = [int(b) for b in tokens[::2]]
    retentions = [int(r) for r in tokens[1::2]]
    if len(breaths) == 0:
        raise ParsingUnitError("at least one round")
    if len(breaths) != len(retentions):
        raise ParsingUnitError(f"breaths and retentions don't match {tokens}")
    if any(x < 0 for x in breaths):
        raise ParsingUnitError("breaths must all be positive")
    if any(x < 0 for x in retentions):
        raise ParsingUnitError("retentions must all be positive")

    return WimhofData(
        rounds=[
            RoundData(round_nr=i, breaths=b, retention=r)
            for i, (b, r) in enumerate(zip(breaths, retentions, strict=False))
        ]
    )
