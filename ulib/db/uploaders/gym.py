from sqlalchemy.orm import Session

# project imports
from ulib.db.tables.gym import GymTable
from ulib.db.uploaders.base import BaseUploader


class GymUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def _upload_unit(self, attrs):
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()
            keiko = GymTable(start_t=attrs.start_t,
                             end_t=attrs.end_t,
                             gym=attrs.gym,
                             fk_unit=self.unit.key)
            session.add(keiko)
            session.commit()
