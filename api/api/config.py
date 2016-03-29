

class Config(object):
    JWT_SECRET_KEY = "change-this-in-production"
    JWT_EXPIRE_TIME = 3600
    JWT_TOKEN_PREFIX = "Bearer"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "change-this-in-production"
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_POOL_SIZE = 5


class Development(Config):
    DEBUG = True
    CORS_DOMAIN = 'markdraft.dev'
    JWT_REFRESH_SECRET = 'also-change-this-in-production'
    JWT_REFRESH_EXPIRY = 7*24*60*60
    APP_NAME = 'markdraft'
    db_uri = "postgresql://vagrant:vagrant@localhost/{0}"
    SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)


class Testing(Config):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    TESTING = True
    APP_NAME = 'markdraft_test'
    db_uri = "postgresql://vagrant:vagrant@localhost/{0}"
    SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
    JWT_REFRESH_SECRET = 'some-random-stuff-for-testing'
    JWT_REFRESH_EXPIRY = 7*24*60*60
