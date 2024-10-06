from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Keiko, GymName, TrainingTopic


class Gym(Keiko):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column(nullable=False)
    end_t: Mapped[float] = mapped_column(nullable=False)
    gym: Mapped[str] = mapped_column(ForeignKey(GymName.name),
                                     nullable=False)
    training: Mapped[str] = mapped_column(ForeignKey(TrainingTopic.name))
