

class KeikoService:
    def __init__(self, unit_repo):
        self.unit_repo = unit_repo

    def get_all_emojis(self):
        rows = self.unit_repo.get_all()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def emoji_for_unit(self, unit_name: str):
        return self.unit_repo.get_emoji_for_unit(unit_name)

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        return self.unit_repo.get_units(unit_name, start_t, end_t)

    def get_category_for_unit(self, unit_name):
        return self.unit_repo.get_category_for_unit(unit_name)

    def create_unit(self, spec):
        emoji_key = self.unit_repo.get_emoji_key_by_unit(spec.unit_name)
        unit = UnitTable(timestamp=spec.timestamp,
                         payload=' '.join(spec.words),
                         comment=spec.comment,
                         fk_emoji=emoji_key)
        return unit

    def upload_units(self, unit_spec):
        pass
