import unittest

from api import config, factories
from models import db, User


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = factories.create_flask_app(config.Testing).test_client()
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
