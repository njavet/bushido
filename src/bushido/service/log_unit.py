from sqlalchemy.orm import Session

from bushido.infra.registry import get_mapper, get_parser, get_repo
from bushido.modules.domain import Err, Ok, Result


def log_unit(line: str, session: Session) -> Result[str]:
    unit_name, payload = line.split(" ", 1)
    parser_res = get_parser(unit_name)
    if isinstance(parser_res, Err):
        return parser_res
    else:
        parser = parser_res.value

    mapper_res = get_mapper(unit_name)
    if isinstance(mapper_res, Err):
        return mapper_res
    else:
        mapper = mapper_res.value

    repo_res = get_repo(unit_name, session)
    if isinstance(repo_res, Err):
        return repo_res
    else:
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
