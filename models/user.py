from models.base_model import BaseModel
import peewee as pw
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re 
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property 


class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False, null=False)
    username = pw.CharField(unique=True, null=False)
    password = None
    password_hash = pw.CharField()
    email = pw.CharField(null=False)
    image_path = pw.TextField(null=True, default="https://images.unsplash.com/photo-1578320339911-5e7974b2720a?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1536&q=80")
    description = pw.TextField(null=True, default="Tell your story.")
    privacy = pw.CharField(default = 1) #1 means user is public; 0 is private 


    @hybrid_property
    def full_image_path(self):
        return AWS_S3_DOMAIN + self.image_path 

    def validate(self):

        if not self.id:
            existing_username = User.get_or_none(User.username == self.username)
            if existing_username is not none:
                    self.errors.append("Sadly, this username has been taken. Please choose another.")
            
            email_existing = User.get_or_none(User.email == self.email)
            if email_existing:
                    self.errors.append("There is an existing account associated with this email.")
            

        if not (self.id and (self.password == None)):
        
            has_lowercase = re.search("[a-z]", self.password)
            has_uppercase = re.search("[A-Z]", self.password)
            has_special_char = re.search("[ \! \" \# \$ \% \& \' \( \) \* \+ \, \- \. \/ \: \; \< \= \> \? \@ \[ \] \\ \^ \_ \` \{ \} \| \~ ]", self.password)

            if has_lowercase and has_uppercase and has_special_char:
                self.password_hash = generate_password_hash(self.password)

            else:
                self.errors.append("Password either has fewer than 6 characters or does not have a lowercase, uppercase, or a special character.")
        
        else:
            pass

