import unittest

from models import User, db
from api import config, app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.Testing)
        db.create_all()
        user = User(
            username="testuser",
            password="123abc",
            first_name="Test",
            last_name="User"
        )
        user.save()
        self.default_user = user

    def tearDown(self):
        db.session.remove()
        db.drop_all()
