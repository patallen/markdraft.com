from api.app import create_app
import config


app = create_app(config.Development)


from api.views import documents, users, tags
from api import errors
