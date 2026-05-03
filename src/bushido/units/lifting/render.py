from .orm import LiftingSet, LiftingUnit


def format_lifting_unit(unit: LiftingUnit) -> str:
    def format_set(s: LiftingSet) -> str:
        if s.weight == int(s.weight):
            weight = str(int(s.weight))
        else:
            weight = str(s.weight)
        if s.reps == int(s.reps):
            reps = str(int(s.reps))
        else:
            reps = str(s.reps)
        if s.rest == 0:
            return " ".join([weight, reps])
        else:
            return " ".join([weight, reps, str(int(s.rest)), ", "])

    return "".join(map(format_set, unit.subunits))
