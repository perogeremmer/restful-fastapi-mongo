from mongoengine import *
from app.models.user import Users


class Todos(Document):
    title = StringField(max_length=200, required=True)
    description = StringField()
    owner = LazyReferenceField(Users, reverse_delete_rule=CASCADE)
