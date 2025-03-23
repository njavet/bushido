def get_emojis(engine):
    stmt = (select(MDEmojiTable.base_emoji,
                   MDEmojiTable.ext_emoji,
                   MDCategoryTable.name,
                   MDEmojiTable.unit_name,
                   MDEmojiTable.key)
            .join(MDCategoryTable))
    emoji_lst = []
    with Session(engine) as session:
        # TODO investigate open session for retrieving keys
        #  -> not bound to a session error
        data = session.execute(stmt).all()
    for item in data:
        byte_seq = item.base_emoji.encode('utf-8')
        base_emoji = byte_seq.decode('unicode_escape')
        if item.ext_emoji is None:
            emoji = base_emoji
        else:
            bs = (item.base_emoji + item.ext_emoji).encode('utf-8')
            emoji = bs.decode('unicode_escape')
        emoji_spec = EmojiProcessor(base_emoji=base_emoji,
                                    emoji=emoji,
                                    category_name=item.name,
                                    unit_name=item.unit_name,
                                    key=item.key)
        emoji_lst.append(emoji_spec)
    return emoji_lst
