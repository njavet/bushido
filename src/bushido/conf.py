from enum import StrEnum

DB_URL = "sqlite:///bushido.persistence"

BUSHIDO_IMG = "src/bushido/assets/images/bushido.png"
KYOKUSHIN_IMG = "src/bushido/assets/images/kyokushin.png"

DEFAULT_PORT = 8000


class UnitType(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"
