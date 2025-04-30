import json
import re

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.data.db_init import db_init
from bushido.service.bot import Bot
from bushido.main import load_log_services


def main():
    with open('units_2023-01-01_2025-03-22.json') as f:
        data = json.load(f)
    db_init()

    log_services = load_log_services()
    bot = Bot(log_services)

    for unit in data:
        emoji = bot.get_emoji_for_unit(unit['unit_name'])
        local_dt = re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})',
               r'\1.\2.\3-\4\5',
               unit['local_datetime'])
        try:
            text = ' '.join([emoji, '--dt', local_dt, unit['payload']])
        except:
            print('emoji', emoji, 'unit', unit['unit_name'])
            continue

        try:
            bot.log_unit(text)
        except ValidationError as e:
            print('error', e.message)
            print(unit['payload'])
            continue
        except KeyError as e:
            print('error', e)
            print(unit['payload'])
            continue


if __name__ == '__main__':
    main()
