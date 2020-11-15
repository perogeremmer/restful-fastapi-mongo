from mongoengine import *

from app.models.todo import Todos
from app.models.user import Users


class TodoLogs(Document):
    message = StringField()
    todo = LazyReferenceField(Todos, reverse_delete_rule=CASCADE)
    user = LazyReferenceField(Users, reverse_delete_rule=CASCADE)
    created_at = DateTimeField()
