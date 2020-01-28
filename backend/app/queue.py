import traceback

import json

import pika

from .config import config
from . import app, redis, config


def queue_push(payload, queue=None):
    if not queue:
        return

    try:
        redis.lpush(queue, json.dumps(payload))
    except:
        app.logger.info('Connection Error')
        traceback.print_exc()
        return


def queue_publish(payload, queue=None):
    if not queue:
        return

    global pika_connection
    try:
        channel = pika_connection.channel()
    except:
        app.logger.info('reconnect')
        pika_connection = pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_URL))
        channel = pika_connection.channel()

    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(payload))