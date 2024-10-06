from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Keiko


class Mind(Keiko):
    seconds = pw.FloatField()
    topic = pw.CharField()
    focus = pw.CharField(null=True)
    # unix utc timestamps
    start_t = pw.FloatField(null=True)
    end_t = pw.FloatField(null=True)
    breaks = pw.IntegerField(null=True)

