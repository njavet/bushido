

def construct_emoji(emoji_base, emoji_ext):
    if emoji_ext is None:
        emoji = emoji_base.encode().decode('unicode-escape')
    else:
        emoji = (emoji_base + emoji_ext).encode().decode('unicode-escape')
    return emoji
