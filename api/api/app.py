from flask import Flask
from data import db

from api.views import auth, documents, tags, users


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(documents.blueprint)
    app.register_blueprint(tags.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(auth.blueprint)
