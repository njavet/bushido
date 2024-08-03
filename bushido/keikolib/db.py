import peewee as pw
import os
import sys
import logging


logger = logging.getLogger(__name__)
database = pw.SqliteDatabase(None)


def init_database(db_name, models):
    # TODO move this code (OS independent, installation code)
    data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
    # init database
    db_url = os.path.join(data_dir, db_name)
    database.init(db_url)

    # create tables
    try:
        database.connect()
    except pw.OperationalError as e:
        logger.error(f'peewee operational error: {e}')
        sys.exit(1)
    else:
        database.create_tables(models=[Unit, Message],
                               safe=True)
        database.create_tables(models=models, safe=True)
    database.close()


class BaseModel(pw.Model):
    class Meta:
        database = database


class Unit(BaseModel):
    category = pw.CharField()
    uname = pw.CharField()
    umoji = pw.CharField()
    # unix utc timestamp
    timestamp = pw.FloatField()


class Keiko(BaseModel):
    """ abstract base class for all keikos """
    unit = pw.ForeignKeyField(Unit)


class Message(BaseModel):
    unit = pw.ForeignKeyField(Unit)
    payload = pw.CharField(null=True)
    comment = pw.TextField(null=True)
