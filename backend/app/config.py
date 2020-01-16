import os


class Config(object):
    DEBUG = os.getenv('FLASK_DEBUG', '').lower() in ['true', 'y', 'yes']
    TESTING = False
    CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    MONGODB_HOST = os.getenv('MONGODB_URI', 'localhost')

    RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/%2F')


config = Config()
