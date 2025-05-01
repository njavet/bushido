from zoneinfo import ZoneInfo
from pathlib import Path

DEFAULT_PORT = 8080

LOCAL_TIME_ZONE = ZoneInfo('Europe/Zurich')

# directories
MASTER_DATA_DIR = Path('bushido', 'static', 'master_data')
ORM_MODELS = 'bushido.data.categories'
KEIKO_PROCESSORS = 'bushido.service.categories'

DB_URL = 'sqlite:///bushido.db'

DAY_START_HOUR = 4
