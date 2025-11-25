# general imports
import peewee as pw

# project imports
import config


class BaseModel(pw.Model):
    class Meta:
        database = pw.SqliteDatabase(config.db_name)


class User(BaseModel):
    user_id = pw.IntegerField(primary_key=True)
    user_name = pw.CharField(default='Platon')


class Unit(BaseModel):
    user_id = pw.ForeignKeyField(User)
    module_name = pw.CharField()
    unit_name = pw.CharField()
    unit_emoji = pw.CharField()
    log_time = pw.DateTimeField()
    comment = pw.TextField(null=True)


class SubUnit(BaseModel):
    unit_id = pw.ForeignKeyField(Unit)


class Message(BaseModel):
    user_id = pw.ForeignKeyField(User)
    msg = pw.TextField()
    log_time = pw.DateTimeField()
    comment = pw.TextField(null=True)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([User, Unit, Message], safe=True)
database.close()
