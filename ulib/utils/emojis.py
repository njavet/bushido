import pandas as pd

# project imports
from ulib.schemas.base import Emoji


def create_emoji_specs(emojis: list) -> list[Emoji]:
    lst = []
    for row in emojis:
        if row.emoji_ext is None:
            base_emoji = row.emoji_base.encode('utf-8').decode('unicode_escape')
            emoji = base_emoji
        else:
            base_emoji = row.emoji_base.encode('utf-8').decode('unicode_escape')
            emoji = (row[0] + row[1]).encode('utf-8').decode('unicode_escape')

        emoji_spec = Emoji(base_emoji=base_emoji,
                           emoji=emoji,
                           category_name=row.name,
                           unit_name=row.unit_name,
                           key=row.key)
        lst.append(emoji_spec)
    return lst


def create_emoji_dix(emojis: list) -> dict:
    emoji_specs = create_emoji_specs(emojis)
    dix = {}
    for emoji_spec in emoji_specs:
        dix[emoji_spec.base_emoji] = emoji_spec
        dix[emoji_spec.emoji] = emoji_spec
    return dix


def prepare_emojis():
    emojis = pd.read_csv('bushido/static/master_data/emojis.csv')
    emojis['emoji_ext'] = emojis['emoji_ext'].fillna('')
    emojis['emoji'] = emojis['emoji_base'] + emojis['emoji_ext']
    emojis['emoji'] = emojis['emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    return emojis
