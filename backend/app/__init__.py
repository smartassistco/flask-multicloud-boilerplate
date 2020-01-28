from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from flask_migrate import Migrate
from flask_admin import Admin

from .config import config

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if config.SENTRY_DSN:
    sentry_sdk.init(config.SENTRY_DSN, integrations=[FlaskIntegration()])

app = Flask(__name__)
app.config.from_object(config)
swagger = Swagger(app)

db = SQLAlchemy(app)
redis = FlaskRedis(app)
migrate = Migrate(app, db)

admin = Admin(app, name='boilerplate', template_mode='bootstrap4')

from .models import *
from .views import *
from .admin import *
