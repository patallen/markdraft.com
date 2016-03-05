from flask import Flask
from flask_script import Manager, Server


def create_flask_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def create_manager(app):
    manager = Manager(app)
    manager.add_command("runserver", Server(host="0.0.0.0", port=8000))
    return manager
