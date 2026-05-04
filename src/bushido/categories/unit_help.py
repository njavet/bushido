from bushido.categories.registry import get_category_help, get_unit_names


class UnitHelpService:
    def __init__(self) -> None:
        self.unit_names = get_unit_names()
        self.category_help = get_category_help()
