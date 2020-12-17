from flask import current_app as app
import datetime, os, urllib.parse
import datetime
from peewee import *
from flask_login import UserMixin
import time
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
# Connect to a Postgres database.
# DATABASE = PostgresqlDatabase('stock_app', host='localhost', port=5432)

if "DATABASE_URL" in os.environ:
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
else:
    DATABASE = os.environ.get('DATABASE_URL') or PostgresqlDatabase('stock_app', host='localhost', port=5432)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])
    class Meta:
        database = DATABASE

class UserActivityLog(Model):
    username = CharField()
    activityType = CharField()
    activity = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

class Watchlist(Model):
    watchlist = ForeignKeyField(User, backref='watchlists')
    watchlistname = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

class Stock(Model):
    user = ForeignKeyField(User, backref='stocks')
    watchlist = ForeignKeyField(Watchlist, backref='stocks')
    stock = CharField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, UserActivityLog, Watchlist, Stock], safe=True)
    print("TABLES Created")
    DATABASE.close()