import json

from bushido.conf import DB_URL
from bushido.exceptions import ValidationError, UploadError
from bushido.data.db_init import db_init
from bushido.data.conn import engine, get_session_context
from bushido.data.categories.lifting import LiftingRepository
from bushido.service.categories.lifting import LogService
from bushido.utils.parsing import preprocess_input


def main():
    with open('units_2023-01-01_2025-03-22.json') as f:
        data = json.load(f)

    units = ['squat', 'deadlift', 'benchpress', 'overheadpress', 'rows', 'curls']
    db_init(engine)
    with get_session_context() as session:
        ur = LiftingRepository(session=session)
        service = LogService(ur)

    for unit in data:
        if unit['unit_name'] in units:
            emoji = ur.get_emoji_for_unit(unit['unit_name'])
            text = ' '.join([emoji, '-dt', str(unit['timestamp']), unit['payload']])
            try:
                emoji, words, comment = preprocess_input(text)
            except ValidationError as e:
                print('pre error', e.message)
                print(unit['payload'])
                continue
            try:
                service.process_unit(unit['unit_name'], words, comment)
            except ValidationError as e:
                print('process error', e.message)
                print(unit['payload'])
            except UploadError as e:
                print('error', e.message)
                print(unit['payload'])


if __name__ == '__main__':
    main()
