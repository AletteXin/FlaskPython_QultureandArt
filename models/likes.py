from playhouse.postgres_ext import PostgresqlExtDatabase
import peewee as pw
from flask_login import UserMixin
from models.base_model import BaseModel
from models.images import Image
from models.user import User 

# db = PostgresqlExtDatabase('user_like_db')


class Likes(BaseModel, UserMixin):

    image = pw.ForeignKeyField(Image)
    liker = pw.ForeignKeyField(User)

