from api.factories import create_flask_app
from api import config


app = create_flask_app(config)


from api.views import documents, users
