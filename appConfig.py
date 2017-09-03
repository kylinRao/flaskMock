class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ':memory:'
    USERNAME = "admin"
    PASSWORD = "default"
    SECRET_KEY = "alsdjfljaldlfalsdjlfjaldsklfjlajsdlf"
    DATABASE = "/Users/user1/PycharmProjects/flaskMock/mock.db"
    static_url_path = ''

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):
    TESTING = True