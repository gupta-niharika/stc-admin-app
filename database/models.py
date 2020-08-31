#sare collection fields idhar hain

from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Article(db.Document):
    name = db.StringField(required=True, unique=True)
    desc = db.StringField(required=True)
    domain = db.StringField(required=True)
    link = db.StringField(required=True)

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=4)
    token = db.ListField(db.StringField())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Feed(db.Document):
    title = db.StringField(required=True)
    desc = db.StringField(required=True)
    link = db.StringField(required=True)
    pic = db.StringField(required=True)

class Resources(db.Document):
    title = db.StringField(required=True)
    link = db.StringField(required=True)
    desc = db.StringField(required=True)
    domain = db.StringField(required=True)

class Project(db.Document):
    title = db.StringField(required=True)
    contributors = db.ListField(db.StringField())
    link = db.StringField(required=True)
    desc = db.StringField(required=True)

class Event(db.Document):
    title = db.StringField(required=True)
    desc = db.StringField(required=True)
    link = db.StringField(required=True)
    pic = db.StringField(required=True)

class Github(db.Document):
    title = db.StringField(required=True)
    link = db.StringField(required=True)
