import os.path

import peewee as pw
import sys
import logging
from settings import db_url, data_dir


logger = logging.getLogger(__name__)


def init_storage(models):
    # create datadir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # create tables
    database = pw.SqliteDatabase(db_url)
    try:
        database.connect()
    except pw.OperationalError as e:
        logger.error(f'peewee operational error: {e}')
        sys.exit(1)
    else:
        database.create_tables(models=[Agent, Unit, Message, TxMindUnit],
                               safe=True)
        database.create_tables(models=models, safe=True)
    database.close()


class BaseModel(pw.Model):
    class Meta:
        database = pw.SqliteDatabase(db_url)


class Agent(BaseModel):
    agent_id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    is_me = pw.BooleanField(default=True)


class Unit(BaseModel):
    agent = pw.ForeignKeyField(Agent)
    module_name = pw.CharField()
    name = pw.CharField()
    emoji = pw.CharField()
    unix_timestamp = pw.FloatField()


class Message(BaseModel):
    unit = pw.ForeignKeyField(Unit)
    unix_timestamp = pw.FloatField()
    payload = pw.CharField(null=True)
    comment = pw.TextField(null=True)


class TxMindUnit(BaseModel):
    agent = pw.ForeignKeyField(Agent)
    name = pw.CharField()
    start_t = pw.FloatField()
    end_t = pw.FloatField()
    seconds = pw.IntegerField(default=0)
    breaks = pw.IntegerField(default=0)


def add_agent(agent_id: int, name: str, is_me=False):
    try:
        agent = Agent.create(agent_id=agent_id,
                             name=name,
                             is_me=is_me)
    except pw.IntegrityError:
        agent = None

    return agent


def get_me():
    try:
        agent = Agent.get(is_me=True)
    except pw.DoesNotExist:
        logger.debug('Agent does not exist...')
        agent = None
    except pw.OperationalError:
        logger.debug('operational error... ')
        agent = None
    return agent


def get_last_timestamp(agent_id) -> int:
    try:
        msg = (Message
               .select(Message.unix_timestamp)
               .join(Unit)
               .where(Message.unit.agent == agent_id)
               .order_by(Message.unix_timestamp.desc())).get()
        return msg.unix_timestamp
    except pw.DoesNotExist:
        return 0

