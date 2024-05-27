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

    def save_unit(self, agent_id, unix_timestamp) -> db.Unit | None:
        self.unit = db.Unit.create(agent_id=agent_id,
                                   module_name=self.module_name,
                                   unit_name=self.unit_name,
                                   unit_emoji=self.unit_emoji,
                                   unix_timestamp=unix_timestamp)
        self.save_subunit()
        return self.unit

    def save_unit_message(self, to_id):
        # TODO fix this bad design
        msg = db.Message.create(from_id=self.unit.agent_id,
                                to_id=to_id,
                                unit_id=self.unit,
                                unix_timestamp=self.unit.unix_timestamp,
                                emoji=self.unit.unit_emoji,
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
