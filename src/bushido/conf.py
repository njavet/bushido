from enum import StrEnum

DB_URL = "sqlite:///bushido.db"

BUSHIDO_IMG = "src/bushido/assets/images/bushido.png"
KYOKUSHIN_IMG = "src/bushido/assets/images/kyokushin.png"


class UnitType(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"
