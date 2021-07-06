from models.base_model import BaseModel
import peewee as pw
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re 
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False, null=False)
    username = pw.CharField(unique=True, null=False)
    password = None
    password_hash = pw.CharField()
    email = pw.CharField(null=False)
    birth_date = pw.DateField(null=False)


    def validate(self):
        email_existing = User.get_or_none(User.email == self.email)
        if email_existing:
            self.errors.append("There is an existing account associated with this email.")
        
        existing_username = User.get_or_none(User.username == self.username)
        if existing_username:
            self.errors.append("Sadly, this username has been taken. Please choose another.")
        
        has_lowercase = re.search("[a-z]", self.password)
        has_uppercase = re.search("[A-Z]", self.password)
        has_special_char = re.search("[ \[ \] \# \$ \% \@ \* \< \&]", self.password)

        if has_lowercase and has_uppercase and has_special_char:
            self.password_hash = generate_password_hash(self.password)

        else:
            self.errors.append("Password either does not have a lowercase, uppercase, or a special character.")

