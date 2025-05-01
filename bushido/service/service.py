# project imports
from bushido.schema.res import UnitLogResponse
from bushido.utils.helpers import load_unit_services
from bushido.utils.dt_functions import create_unit_response_dt
from bushido.utils.parsing import (preprocess_input,
                                   parse_datetime_to_timestamp)
from bushido.data.repo import Repository


def log_unit(text, session):
    emoji, words, comment = preprocess_input(text)
    timestamp, words = parse_datetime_to_timestamp(words)
    bushido_date, hms = create_unit_response_dt(timestamp)
    repo = Repository(session)
    unit_name = repo.get_unit_name_for_emoji(emoji)
    category = repo.get_category_for_unit(unit_name)
    log_service = unit_services[category](self.repo)
    log_service.process_unit(unit_name, words, timestamp, comment)
    return UnitLogResponse(date=bushido_date,
                           hms=hms,
                           emoji=emoji,
                           unit_name=unit_name,
                           payload=' '.join(words))


