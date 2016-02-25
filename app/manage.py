from flask_migrate import Migrate, MigrateCommand

from api import app
from api.factories import create_manager
from models import db
import fakedata


manager = create_manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

from models import *


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


if __name__ == "__main__":
    manager.run()
