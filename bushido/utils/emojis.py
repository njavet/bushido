import pandas as pd
import ast

def decode_unicode_emoji(code):
    return ast.literal_eval(f"'{code}'") if pd.notnull(code) else ''


def decode(df):
    df['emoticon'] = df['emoji_base'].apply(decode_unicode_emoji)
    df['emoji'] = df['emoticon'] + df['emoji_ext'].apply(decode_unicode_emoji)
    return df.drop(columns=['emoji_base', 'emoji_ext'])
