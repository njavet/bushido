import json

from bushido.conf import LOCAL_TIME_ZONE, DB_URL
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec
from bushido.data.manager import DataManager
from bushido.data.db_init import db_init
from bushido.service.units import UnitProcessor


def create_unit_spec(timestamp, unit_name, words, comment):
    unit_spec = UnitSpec(timestamp=timestamp,
                         unit_name=unit_name,
                         words=words,
                         comment=comment)
    return unit_spec


def main():
    with open('units_2023-01-01_2025-03-22.json') as f:
        data = json.load(f)

    units = ['squat', 'deadflit', 'benchpress', 'weights', 'scale', 'wimhof']
    dm = DataManager(DB_URL)
    db_init(dm.engine)
    up = UnitProcessor(dm)

    for unit in data:
        if unit['unit_name'] in units:
            emoji = dm.unit_name_to_emoji(unit['unit_name'])
            try:
                unit_name, words, comment = up.preprocess_input(emoji + ' ' + unit['payload'])
            except ValidationError as e:
                print('error', e.message)
                print(unit['payload'])
                continue
            try:
                unit_spec = create_unit_spec(unit['timestamp'],
                                             unit['unit_name'],
                                             words,
                                             comment)
                up.process_input(unit_spec)
            except ValidationError as e:
                print('error', e.message)
                print(unit['payload'])
            except UploadError as e:
                print('error', e.message)
                print(unit['payload'])


if __name__ == '__main__':
    main()
