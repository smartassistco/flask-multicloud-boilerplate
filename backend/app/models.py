import datetime

import flask_mongoengine as mo
import mongoengine


class Task(mo.Document):
    name = mongoengine.StringField()
    status = mongoengine.StringField(default='initialized')
    create_timestamp = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    update_timestamp = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
