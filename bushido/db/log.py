from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Keiko



class Chrono(Keiko):
    seconds: Mapped[float] = mapped_column(nullable=False)

class Mind(Keiko):
    seconds = pw.FloatField()
    topic = pw.CharField()
    focus = pw.CharField(null=True)
    # unix utc timestamps
    start_t = pw.FloatField(null=True)
    end_t = pw.FloatField(null=True)
    breaks = pw.IntegerField(null=True)


class Log(Keiko):
    log_str = pw.CharField()

class Cardio(Keiko):
    # TODO switch to unix utc timestamps
    start_t = pw.TimeField()
    seconds = pw.FloatField()
    gym = pw.CharField()
    distance = pw.FloatField(null=True)
    cal = pw.IntegerField(null=True)
    avghr = pw.IntegerField(null=True)
    maxhr = pw.IntegerField(null=True)

