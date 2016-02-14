from flask_migrate import Migrate, MigrateCommand
from api import app
from api.factories import create_manager
from models import db


manager = create_manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
