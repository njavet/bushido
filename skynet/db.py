# general imports
import datetime
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
    # a unit that is logged after midnight before sleeping
    # should count for the last day, 0400-0359 is the day time span
    log_date = pw.DateField()
    comment = pw.TextField(null=True)

    def set_time(self, recv_time):
        if recv_time is None:
            self.log_time = datetime.datetime.now()
        else:
            self.log_time = recv_time

        if datetime.time(0) < self.log_time.time() < datetime.time(config.day_start):
            # should count for the last day
            self.log_date = self.log_time.date() - datetime.timedelta(days=1)
        else:
            self.log_date = self.log_time.date()


class SubUnit(BaseModel):
    unit_id = pw.ForeignKeyField(Unit)


class Message(BaseModel):
    user_id = pw.ForeignKeyField(User)
    msg = pw.TextField()
    comment = pw.TextField(null=True)
    log_time = pw.DateTimeField()


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([User, Unit, Message], safe=True)
database.close()
