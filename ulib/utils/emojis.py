from pathlib import Path
import pandas as pd


def prepare_emojis(csv_path=Path('ulib/resources/emojis.csv')):
    emojis = pd.read_csv(csv_path)
    emojis['ext_emoji'] = emojis['ext_emoji'].fillna('')
    emojis['emoji'] = emojis['base_emoji'] + emojis['ext_emoji']
    emojis['emoji'] = emojis['emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    return emojis
