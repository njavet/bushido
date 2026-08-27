from enum import StrEnum

# sunday
WEEK_START_DAY = 6

# 0400
DAY_START_HOUR = 4

# e.g. 1600
MILITARY_TIME_LEN = 4

# e.g. 05
MINUTE_LEN = 2

# e.g. 05:00:00
COMPLETE_TIME_LEN = 3


class UnitCategory(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"
