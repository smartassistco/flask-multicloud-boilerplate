import datetime

import sqlalchemy as sa

from . import db


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.String(16))
    create_timestamp = sa.Column(sa.DateTime)
    update_timestamp = sa.Column(sa.DateTime)
