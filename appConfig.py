class Config(object):
    import os
    parpath = os.path.dirname(__file__)
    DEBUG = False
    TESTING = False
    DATABASE_URI = ':memory:'
    USERNAME = "admin"
    PASSWORD = "default"
    SECRET_KEY = "alsdjfljaldlfalsdjlfjaldsklfjlajsdlf"
    DATABASE = os.path.join(parpath,"mock.db")
    static_url_path = ''
    PDFPATH = "pdf"
    STATICPATH = "static"

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):
    TESTING = True