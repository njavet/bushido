import pandas as pd

# project imports
from ulib.schemas.base import Emoji




def prepare_emojis():
    emojis = pd.read_csv('bushido/static/master_data/emojis.csv')
    emojis['emoji_ext'] = emojis['emoji_ext'].fillna('')
    emojis['emoji'] = emojis['emoji_base'] + emojis['emoji_ext']
    emojis['emoji'] = emojis['emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    return emojis
