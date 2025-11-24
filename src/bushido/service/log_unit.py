from sqlalchemy.orm import Session

from bushido.modules.dtypes import Err, Ok, Result
from bushido.modules.factory import get_mappers, get_parsers, get_repo


def log_unit(line: str, session: Session) -> Result[str]:
    # TODO redesign / validation
    unit_name, payload = line.split(" ", 1)
    parsers = get_parsers()
    mappers = get_mappers()
    parser = parsers.get(unit_name)
    mapper = mappers.get(unit_name)

    repo = get_repo(unit_name, session)
    parse_res = parser.parse(payload)
    if isinstance(parse_res, Err):
        return parse_res
    else:
        parsed_unit = parse_res.value

    unit, subunits = mapper.to_orm(parsed_unit)
    if repo.add_unit(unit, subunits):
        return Ok("Unit confirmed")
    else:
        return Err("error")
