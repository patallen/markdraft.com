import unittest

from models import User, db
from api import config, app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.Testing)
        self.app = app.test_client()
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

    def assertAllIn(self, theirs, ours):
        for val in ours:
            if val not in theirs:
                raise AssertionError("Expected %s in list." % (val,))

    def assertStatus(self, response, expected):
        if response.status_code != expected:
            raise AssertionError(
                "Expected status_code to be %s, got %s."
                % (expected, response.status_code)
            )

    def assertStatus200(self, response):
        self.assertStatus(response, 200)
