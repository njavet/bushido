import peewee as pw
import sys
import logging
from blinker import signal


logger = logging.getLogger(__name__)
database = pw.SqliteDatabase(None)
unit_logged = signal('unit_logged')


def init_database(db_url, models):
    # init database
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
    unix_timestamp = pw.FloatField()


class Keiko(BaseModel):
    """ abstract base class for all keikos """
    unit = pw.ForeignKeyField(Unit)


class Message(BaseModel):
    unit = pw.ForeignKeyField(Unit)
    payload = pw.CharField(null=True)
    comment = pw.TextField(null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        unit_logged.send(self)
