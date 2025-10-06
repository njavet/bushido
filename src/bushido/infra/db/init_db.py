from pathlib import Path

from platformdirs import PlatformDirs

APP_NAME = "bushido"
dirs = PlatformDirs(APP_NAME, appauthor=False)


def get_db_path() -> Path:
    state_dir = Path(dirs.user_state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "bushido.sqlite3"
