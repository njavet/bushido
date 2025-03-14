from pathlib import Path
import pandas as pd


def extend_emoji_df(csv_path=Path('bushido/static/csv_files/emojis.csv')):
    emojis = pd.read_csv(csv_path)
    emojis['ext_emoji'] = emojis['ext_emoji'].fillna('')
    emojis['double'] = emojis['base_emoji'] + emojis['ext_emoji']
    emojis['double'] = emojis['double'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    emojis['single'] = emojis['base_emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    emojis['is_unique'] = emojis['double'] == emojis['single']
    return emojis


def get_convert_dict(csv_path=Path('bushido/static/csv_files/emojis.csv')):
    emojis = extend_emoji_df(csv_path=csv_path)
    emojis = emojis.drop(columns=['ext_emoji', 'base_emoji'])
    dix = {}
