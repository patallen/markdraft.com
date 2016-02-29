

class Config(object):
    JWT_SECRET_KEY = "change-this-in-production"
    JWT_EXPIRE_TIME = 3600
    JWT_TOKEN_PREFIX = "Bearer"

    SECRET_KEY = "change-this-in-production"
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_POOL_SIZE = 5


class Development(Config):
    DEBUG = True
    APP_NAME = 'markdraft'
    db_uri = "postgresql://markdraft:markdraft@postgres/{0}"
    SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)


class Testing(Config):
    DEBUG = True
    TESTING = True
    APP_NAME = 'markdraft_test'
    db_uri = "postgresql://markdraft:markdraft@postgres/{0}"
    SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
