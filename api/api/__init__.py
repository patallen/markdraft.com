from api.app import create_app, create_redis
import config


app = create_app(config.Development)
redis = create_redis(config.Development)


from api.views import documents, users, tags
from api import errors
