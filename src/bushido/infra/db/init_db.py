from pathlib import Path

from platformdirs import PlatformDirs

from bushido.infra.db.conn import SessionFactory

APP_NAME = "bushido"
dirs = PlatformDirs(APP_NAME, appauthor=False)


def get_db_path() -> Path:
    state_dir = Path(dirs.user_state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "bushido.sqlite3"


def init_db() -> Path:
    db_path = get_db_path()
    print("Creating database at {}".format(db_path))
    if not db_path.exists():
        sf = SessionFactory(db_path)
        sf.init_db()
        db_path.chmod(0o600)
    return db_path
