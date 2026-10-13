from sqlalchemy.orm import Session

from citadel.bcl import preparse
from citadel.persistence.models import Spartan


def process_command(line: str, session: Session, spartan: Spartan):
    preparsed_cmd = preparse(line)
