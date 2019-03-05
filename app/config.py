import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Development(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:supersecure@db/test_shopee' #os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': Development,
    'testing': Testing
}
