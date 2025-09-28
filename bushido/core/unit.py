from enum import StrEnum


class LiftingUnitName(StrEnum):
    squat = 'squat'
    deadlift = 'deadlift'
    benchpress = 'benchpress'
    overheadpress = 'overheadpress'
    rows = 'rows'


class GymUnitName(StrEnum):
    weights = 'weights'
    martial_arts = 'martial_arts'
    yoga = 'yoga'
