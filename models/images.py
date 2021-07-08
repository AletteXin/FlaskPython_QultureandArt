from models.base_model import BaseModel
import peewee as pw
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re 
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property 
from models.user import User 


class Image(UserMixin, BaseModel):
    image_path = pw.TextField(null=False)
    description = pw.CharField()
    user = pw.ForeignKeyField(User, backref = "users")

    @hybrid_property
    def full_image_path(self):
        return AWS_S3_DOMAIN + self.image_path 