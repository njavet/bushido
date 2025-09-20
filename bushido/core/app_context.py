from bushido.db.conn import SessionFactory


class  AppContext:
    db = dict[str, SessionFactory] | None


app_context = AppContext()
