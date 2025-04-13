class UnitService:
    def __init__(self, repo):
        self.repo = repo

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        return self.repo.get_units(unit_name, start_t, end_t)
