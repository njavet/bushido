from typing import TypeVar

from bushido.infra.db.model.base import Subunit

# generic result type
RT = TypeVar('RT')

# generic type for orm objects
ORM_T = TypeVar('ORM_T', bound=Subunit)

# generic unit type
UNIT_T = TypeVar('UNIT_T')
