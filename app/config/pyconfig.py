class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#
class DevelopmentConfiguration(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1:5432/agendaAPI'
    SECRET_KEY = 'some-random-string'
    JWT_SECRET_KEY = 'some-random-secret-key'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'SOME-RANDOM-KEY'
