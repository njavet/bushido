# project imports
from bushido.service.unit import BaseUnitService
from bushido.service.log import LogService


def get_categories(session):
    service = BaseUnitService.from_session(session)
    return service.get_all_categories()


def get_emojis(session):
    service = BaseUnitService.from_session(session)
    return service.get_all_emojis()


def get_units(session):
    service = BaseUnitService.from_session(session)
    return service.get_all_units()


def log_unit(text, session):
    service = LogService.from_session(session)
    unit_log_res = service.log_unit(text)
    return unit_log_res
