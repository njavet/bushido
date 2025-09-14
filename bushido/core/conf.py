from zoneinfo import ZoneInfo
from pathlib import Path

DEFAULT_PORT = 8080

LOCAL_TIME_ZONE = ZoneInfo('Europe/Zurich')

DAY_START_HOUR = 4

# directories
MASTER_DATA_DIR = Path('bushido', 'static', 'master_data')

DB_URL = 'sqlite:///bushido.db'

