from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Registry:
    pass


UNIT_REGISTRY: dict[str, Registry] = {}
