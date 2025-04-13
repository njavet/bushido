class CategoryService:
    def __init__(self, repo):
        self.repo = repo

    def get_category_for_unit(self, unit_name):
        return self.repo.get_category_for_unit(unit_name)
