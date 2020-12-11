import datetime
from peewee import *
from flask_login import UserMixin
# Connect to a Postgres database.
DATABASE = PostgresqlDatabase('stock_app', host='localhost', port=5432)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE

class UserActivityLog(Model):
    username = CharField()
    activity = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, UserActivityLog], safe=True)
    print("TABLES Created")
    DATABASE.close()