import pika as pika
from flasgger import Swagger
from flask import Flask
from flask_mongoengine import MongoEngine
from .config import config

app = Flask(__name__)
app.config.from_object(config)
swagger = Swagger(app)

db = MongoEngine(app)

pika_connection = pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_URL))
pika_channel = pika_connection.channel()
pika_channel.queue_declare('initialized')
pika_channel.queue_declare('processing')

from .models import *
from .views import *
