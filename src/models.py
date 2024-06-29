from peewee import Model, CharField, IntegerField, ForeignKeyField, SqliteDatabase, DateTimeField
from src.utils import hash_password, verify_password
import datetime

db = SqliteDatabase('data.db')


class User(Model):

    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

    def check_password(self, password):
        return verify_password(str(self.password), password)

    @classmethod
    def create_user(cls, username, password):

        hashed_password = hash_password(password)

        if cls.user_exists(username):
            return False

        try:
            return cls.create(
                username=username,
                password=hashed_password
            )
        except Exception as e:
            print(e)
            return False

    @classmethod
    def user_exists(cls, username):
        return cls.select().where(cls.username == username).exists()




class Score(Model):

    user = ForeignKeyField(User, backref='scores')
    value = IntegerField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def create_tables():
    db.connect()
    db.create_tables([User, Score])