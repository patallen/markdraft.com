from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell

from data.models import User
from api import app
from data import db

import fakedata

manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    return {'app': app, 'db': db, 'User': User}


@manager.command
def fake_users():
    fakedata.fake_users()


@manager.command
def fake_documents(verbose=True):
    fakedata.fake_documents(verbose=verbose)


@manager.command
def fake_shares(verbose=True):
    fakedata.fake_shares(verbose=verbose)


@manager.command
def fake_all(verbose=True):
    fake_users()
    fake_documents(verbose=verbose)
    fake_shares(verbose=verbose)


manager.add_command("db", MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))


if __name__ == "__main__":
    manager.run()
