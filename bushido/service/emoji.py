from bushido.data.base_repo import BaseRepository


class EmojiService:
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def get_all_emojis(self):
        rows = self.repo.get_all_emojis()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]
