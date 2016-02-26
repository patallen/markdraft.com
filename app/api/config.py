APP_NAME = 'markdraft'

JWT_SECRET_KEY = "dlkjfkasdklfjdaslkfjdak9"
JWT_EXPIRE_TIME = 3600
SECRET_KEY = "kdjsf93uef09ifewdjasj0923"
DEBUG = True
TESTING = True
LOG_LEVEL = 'DEBUG'
db_uri = "postgresql://markdraft:markdraft@postgres/{0}"
SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
SQLALCHEMY_POOL_SIZE = 5
