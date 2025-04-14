import json

from bushido.conf import DB_URL
from bushido.exceptions import ValidationError, UploadError
from bushido.data.db_init import db_init


def main():
    with open('units_2023-01-01_2025-03-22.json') as f:
        data = json.load(f)

    units = ['squat', 'deadlift', 'benchpress', 'overheadpress', 'rows', 'curls']
    db_init(dm.engine)

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
