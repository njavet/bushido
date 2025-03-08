from sqlalchemy.orm import Session

# project imports
from ulib.db.uploaders.base import BaseUploader
from ulib.db.tables.lifting import LiftingTable


class LiftingUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def _upload_unit(self, attrs):
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()
            keikos = []
            for set_nr, w, r, p in attrs.zipped():
                lifting = LiftingTable(set_nr=set_nr,
                                       weight=w,
                                       reps=r,
                                       pause=p,
                                       fk_unit=self.unit.key)
                keikos.append(lifting)
            session.add_all(keikos)
            session.commit()
