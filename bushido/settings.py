import os
from dotenv import load_dotenv
load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('T800_TOKEN')
data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
db_url = os.path.join(data_dir, 'bushido.db')
t800_session = os.path.join(data_dir, 't800.session')
agent_session = os.path.join(data_dir, 'bushido.session')


# day starts at 0400
day_start = 4
