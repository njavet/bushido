from bushido.db.conn import SessionFactory


class AppContext:
    dbs = dict[str, SessionFactory] | None


app_context = AppContext()
