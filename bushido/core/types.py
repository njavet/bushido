from typing import TypeVar, Protocol

from bushido.db.model.base import Unit, Subunit


# generic result type
RT = TypeVar('RT')

# generic type for orm objects
ORM_T = TypeVar('ORM_T', bound=Unit)
ORM_ST = TypeVar('ORM_ST', bound=Subunit)

# generic unit type
UNIT_T = TypeVar('UNIT_T')

