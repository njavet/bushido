from pydantic import BaseModel
import pandas as pd


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


def prepare_emojis():
    emojis = pd.read_csv('bushido/static/master_data/emojis.csv')
    emojis['emoji_ext'] = emojis['emoji_ext'].fillna('')
    emojis['emoji'] = emojis['emoji_base'] + emojis['emoji_ext']
    emojis['emoji'] = emojis['emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    return emojis
