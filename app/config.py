import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Development(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')

    TESTING = True
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': Development,
    'testing': Testing
}
