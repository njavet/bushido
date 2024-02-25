import unitproc
import db


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = db.ChronoUnit


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        self.unit_model = db.ChronoUnit

