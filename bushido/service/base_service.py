from bushido.data.base_repo import BaseRepository


class BaseService:
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def get_all_emojis(self):
        rows = self.repo.get_all_emojis()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def emoji_for_unit(self, unit_name: str):
        return self.repo.get_emoji_for_unit(unit_name)

    def unit_name_for_emoji(self, emoji: str):
        return self.repo.get_unit_name_for_emoji(emoji)

    def get_category_for_unit(self, unit_name):
        return self.repo.get_category_for_unit(unit_name)
