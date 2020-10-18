from mongoengine import *


class Users(Document):
    name = StringField(max_length=200, required=True)
