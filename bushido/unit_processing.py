import abc
from dataclasses import dataclass
import peewee as pw

# project imports
import db


class UnitProcessor(abc.ABC):
    def __init__(self, module_name, unit_name, unit_emoji) -> None:
        self.module_name = module_name
        self.unit_name = unit_name
        self.unit_emoji = unit_emoji
        # TODO is there a name / pattern for this mechanism ? the field
        #  unit and subunit serve as temporary storage, is it good / bad ?
        #  properties, clean OO
        self.unix_timestamp = None
        self.payload = None
        self.comment = None
        self.attrs: Attrs | None = None
        self.unit: db.Unit | None = None
        self.subunit: SubUnit | None = None

    def parse_words(self, words: list) -> None:
        """
        every unit has to override this function to its specific format
        :param words:
        :return:
        """
        raise NotImplementedError

    def save_unit(self, agent_id) -> db.Unit | None:
        self.unit = db.Unit.create(agent_id=agent_id,
                                   module_name=self.module_name,
                                   name=self.unit_name,
                                   emoji=self.unit_emoji,
                                   unix_timestamp=self.unix_timestamp)
        self.save_subunit()
        return self.unit

    def save_unit_message(self, unix_timestamp):
        # TODO fix this bad design
        msg = db.Message.create(unit_id=self.unit,
                                unix_timestamp=unix_timestamp,
                                payload=self.payload,
                                comment=self.comment)
        return msg

    def save_subunit(self):
        raise NotImplementedError


@dataclass
class Attrs:
    pass


class SubUnit(db.BaseModel):
    unit_id = pw.ForeignKeyField(db.Unit)
