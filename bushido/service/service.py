# project imports
from bushido.service.loader import load_unit_service
from bushido.service.unit import BaseUnitService
from bushido.service.log import LogService


def get_categories(session):
    service = BaseUnitService.from_session(session)
    return service.get_all_categories()


def get_emojis(session):
    service = BaseUnitService.from_session(session)
    return service.get_all_emojis()


def get_units(session, category=None):
    if category is None:
        service = BaseUnitService.from_session(session)
    else:
        cls = load_unit_service(category)
        service = cls(session)
    return service.get_units_by_day()


def log_unit(text, session):
    service = LogService.from_session(session)
    unit_log_res = service.log_unit(text)
    return unit_log_res

