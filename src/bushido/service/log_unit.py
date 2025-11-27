from sqlalchemy.orm import Session

from bushido.core.result import Err, Ok, Result
from bushido.modules.dtypes import ParsedUnit
from bushido.modules.factory import Factory


class LogUnit:
    def __init__(self, factory: Factory):
        self.factory = factory

    def log_unit(self, line: str, session: Session) -> Result[ParsedUnit]:
        try:
            unit_name, payload = line.split(" ", 1)
        except ValueError:
            unit_name, payload = line, ""

        # fetch log classes
        parser_res = self.factory.get_parser(unit_name)
        if isinstance(parser_res, Err):
            return parser_res
        parser = parser_res.value

        mapper_res = self.factory.get_mapper(unit_name)
        if isinstance(mapper_res, Err):
            return mapper_res
        mapper = mapper_res.value

        repo_res = self.factory.get_repo(unit_name, session)
        if isinstance(repo_res, Err):
            return repo_res
        repo = repo_res.value

        # parse and store
        parse_res = parser.parse(payload)
        if isinstance(parse_res, Err):
            return parse_res
        else:
            parsed_unit = parse_res.value

        unit, subunits = mapper.to_orm(parsed_unit)
        if repo.add_unit(unit, subunits):
            return Ok(parsed_unit)
        else:
            return Err("error")
