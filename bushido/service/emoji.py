class EmojiService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_emojis(self):
        rows = self.repo.get_all()
        return [dict(emoji=r.emoji, unit_name=r.unit_name) for r in rows]

    def emoji_for_unit(self, unit_name: str):
        return self.repo.get_emoji_for_unit(unit_name)
