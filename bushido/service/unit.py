from bushido.data.models import UnitTable


class UnitService:
    def __init__(self, unit_repo, emoji_repo):
        self.unit_repo = unit_repo
        self.emoji_repo = emoji_repo

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        return self.unit_repo.get_units(unit_name, start_t, end_t)

    def get_category_for_unit(self, unit_name):
        return self.unit_repo.get_category_for_unit(unit_name)

    def create_unit(self, spec):
        emoji_key = self.emoji_repo.get_emoji_key_by_unit(spec.unit_name)
        unit = UnitTable(timestamp=spec.timestamp,
                         payload=' '.join(spec.words),
                         comment=spec.comment,
                         fk_emoji=emoji_key)
        return unit

    def upload_units(self, unit_spec):
        pass
