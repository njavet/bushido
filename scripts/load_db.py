from collections import defaultdict
import json
import re

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.data.db_init import db_init
from bushido.service.bot import Bot
from bushido.service.unit import BaseUnitService


def main():
    with open('units_2023-01-01_2025-03-22.json') as f:
        data = json.load(f)
    db_init()

    bot = Bot()
    repo = bot.get_repo()
    service = BaseUnitService(repo)

    errors = defaultdict(list)
    for unit in data:
        emoji = service.get_emoji_for_unit(unit['unit_name'])
        local_dt = re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})',
               r'\1.\2.\3-\4\5',
               unit['local_datetime'])
        try:
            text = ' '.join([emoji, '--dt', local_dt, unit['payload']])
        except:
            errors[unit['unit_name']].append(unit['payload'])
            continue

        try:
            bot.log_unit(text)
        except ValidationError as e:
            errors[unit['unit_name']].append(unit['payload'])
            continue
        except KeyError as e:
            errors[unit['unit_name']].append(unit['payload'])
            continue

    for k, v in errors.items():
        print(k)
        print('------')

if __name__ == '__main__':
    main()
