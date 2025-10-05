from pathlib import Path

from platformdirs import PlatformDirs

APP = "bushido"
_dirs = PlatformDirs(APP, appauthor=False)


def ensure_dirs() -> tuple[Path, Path, Path]:
    cfg = Path(_dirs.user_config_dir)
    state = Path(_dirs.user_state_dir)
    cache = Path(_dirs.user_cache_dir)
    for p in (cfg, state, cache):
        p.mkdir(parents=True, exist_ok=True)
    return cfg, state, cache


def db_path() -> Path:
    _, state, _ = ensure_dirs()
    return state / "bushido.sqlite3"
