from sqlalchemy.orm import Session

from bushido.modules.dtypes import Err, Ok, Result
from bushido.modules.factory import Factory


def log_unit(line: str, factory: Factory, session: Session) -> Result[str]:
    try:
        unit_name, payload = line.split(" ", 1)
    except ValueError:
        unit_name, payload = line, ""

    parser_res = factory.get_parser(unit_name)
    if isinstance(parser_res, Err):
        return parser_res
    parser = parser_res.value
    mapper_res = factory.get_mapper(unit_name)
    if isinstance(mapper_res, Err):
        return mapper_res
    mapper = mapper_res.value

    repo_res = factory.get_repo(unit_name, session)
    if isinstance(repo_res, Err):
        return repo_res
    repo = repo_res.value
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
