from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Keiko



class Chrono(Keiko):
    seconds: Mapped[float] = mapped_column(nullable=False)


class Cardio(Keiko):
    # TODO switch to unix utc timestamps
    start_t = pw.TimeField()
    seconds = pw.FloatField()
    gym = pw.CharField()
    distance = pw.FloatField(null=True)
    cal = pw.IntegerField(null=True)
    avghr = pw.IntegerField(null=True)
    maxhr = pw.IntegerField(null=True)

