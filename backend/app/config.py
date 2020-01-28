import os


class Config(object):
    DEBUG = os.getenv('FLASK_DEBUG', '').lower() in ['true', 'y', 'yes']
    TESTING = os.getenv('FLASK_TESTING', '').lower() in ['true', 'y', 'yes']
    CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_KEY = os.getenv('API_KEY')

    POSTGRES_URL = os.getenv('POSTGRES_URL', 'sqlite://')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    SQLALCHEMY_DATABASE_URI = POSTGRES_URL

    SENTRY_DSN = os.getenv('SENTRY_DSN', '')


config = Config()
