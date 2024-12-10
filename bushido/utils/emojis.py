from pydantic import BaseModel


class EmojiSpec(BaseModel):
    base_emoji: str
    emoji: str
    unit_name: str
    category: str


def format_emojis(emojis: list) -> list[EmojiSpec]:
    lst = []
    for row in emojis:
        if row[1]:
            base_emoji = row[0].encode('utf-8').decode('unicode_escape')
            emoji = (row[0] + row[1]).encode('utf-8').decode('unicode_escape')
        else:
            base_emoji = row[0].encode('utf-8').decode('unicode_escape')
            emoji = base_emoji

        emoji_spec = EmojiSpec(base_emoji=base_emoji,
                               emoji=emoji,
                               category=row[2],
                               unit_name=row[3])

        lst.append(emoji_spec)
    return lst

