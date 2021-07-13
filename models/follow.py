from playhouse.postgres_ext import PostgresqlExtDatabase
import peewee as pw
from flask_login import UserMixin
from models.base_model import BaseModel
from models.user import User 

# db = PostgresqlExtDatabase('follow_db')


class Follow(BaseModel, UserMixin):

    idol = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    approved = pw.CharField(default = "0")

# user1 = User.get_or_none(User.id == "17")
# user2 = User.get_or_none(User.id == "20")
# user3 = User.get_or_none(User.id == "18")

# Follow.create(idol = user1, follower = user2)
# Follow.create(idol = user3, follower = user2)
# Follow.create(idol = user3, follower = user1)


# Follow.get_or_none(Follow.id ).delete_instance()


# user = User.select().first()
# idols = User.select().join(Follow, on = Follow.follower_id == User.id).where(Follow.idol == user)
# print([i for i in followers])
