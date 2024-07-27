import peewee as pw
import os
import sys
import logging


logger = logging.getLogger(__name__)
database = pw.SqliteDatabase(None)


def init_database(db_url, models):
    # init database
    data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
    db_url = os.path.join(data_dir, 'bushido.db')
    database.init(db_url)

    # create tables
    try:
        database.connect()
    except pw.OperationalError as e:
        logger.error(f'peewee operational error: {e}')
        sys.exit(1)
    else:
        database.create_tables(models=[Budoka, Unit, Message],
                               safe=True)
        database.create_tables(models=models, safe=True)
    database.close()


class BaseModel(pw.Model):
    class Meta:
        database = database


class Budoka(BaseModel):
    budoka_id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    is_me = pw.BooleanField(default=True)


class Unit(BaseModel):
    budoka = pw.ForeignKeyField(Budoka)
    category = pw.CharField()
    uname = pw.CharField()
    umoji = pw.CharField()
    timestamp = pw.FloatField()


class Message(BaseModel):
    unit = pw.ForeignKeyField(Unit)
    payload = pw.CharField(null=True)
    comment = pw.TextField(null=True)


def add_budoka(budoka_id: int, name: str, is_me=False) -> Budoka | None:
    try:
        budoka = Budoka.create(budoka_id=budoka_id,
                               name=name,
                               is_me=is_me)
    except pw.IntegrityError:
        budoka = None

    return budoka


def get_me() -> Budoka | None:
    try:
        budoka = Budoka.get(is_me=True)
    except pw.DoesNotExist:
        logger.debug('Budoka does not exist...')
        budoka = None
    except pw.OperationalError:
        logger.debug('operational error... ')
        budoka = None
    return budoka
