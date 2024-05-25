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

    def save_unit(self, tg_message_data) -> db.Unit | None:
        self.unit = db.Unit.create(agent_id=tg_message_data.from_id,
                                   module_name=self.module_name,
                                   unit_name=self.unit_name,
                                   unit_emoji=self.unit_emoji,
                                   log_time=tg_message_data.log_time,
                                   unix_timestamp=tg_message_data.unix_timestamp)
        return self.unit

    def save_unit_message(self, tg_message_data):
        msg = db.Message.create(msg_id=tg_message_data.msg_id,
                                from_id=tg_message_data.from_id,
                                to_id=tg_message_data.to_id,
                                unit_id=self.unit,
                                log_time=tg_message_data.log_time,
                                unix_timestamp=tg_message_data.unix_timestamp,
                                emoji_payload=tg_message_data.emoji_payload,
                                comment=tg_message_data.comment)
        return msg

    def save_subunit(self):
        raise NotImplementedError


@dataclass
class Attrs:
    pass


class SubUnit(db.BaseModel):
    unit_id = pw.ForeignKeyField(db.Unit)
