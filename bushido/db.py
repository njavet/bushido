import asyncio

import peewee as pw
from playhouse.signals import Model, post_save, post_delete
import sys
import os
import logging

# project imports
import config
import helpers


logger = logging.getLogger(__name__)


def get_database():
    data_dir_path = helpers.get_data_dir_path()
    db_path = os.path.join(data_dir_path, config.db_name)
    database = pw.SqliteDatabase(db_path)
    return database


def init_storage(models):
    # create user data dir
    helpers.create_user_data_dir()
    # create tables
    database = get_database()
    try:
        database.connect()
    except pw.OperationalError as e:
        logger.error(f'peewee operational error: {e}')
        sys.exit(1)
    else:
        database.create_tables([Agent, Unit, Message], safe=True)
        database.create_tables(models, safe=True)
    database.close()


class BaseModel(pw.Model):
    class Meta:
        database = get_database()


class Agent(BaseModel):
    agent_id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    is_me = pw.BooleanField(default=True)


class Unit(BaseModel):
    agent_id = pw.ForeignKeyField(Agent)
    module_name = pw.CharField()
    unit_name = pw.CharField()
    unit_emoji = pw.CharField()
    log_time = pw.DateTimeField()
    unix_timestamp = pw.FloatField()


class Message(BaseModel):
    msg_id = pw.IntegerField()
    from_id = pw.ForeignKeyField(Agent)
    to_id = pw.ForeignKeyField(Agent)
    unit_id = pw.ForeignKeyField(Unit)
    emoji_payload = pw.TextField()
    log_time = pw.DateTimeField()
    unix_timestamp = pw.FloatField()
    comment = pw.TextField(null=True)


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


def get_last_msg_id(agent_id) -> int:
    try:
        msg = (Message
               .select(Message.msg_id)
               .where(Message.from_id == agent_id)).get()
        return msg.msg_id
    except pw.DoesNotExist:
        return 0

