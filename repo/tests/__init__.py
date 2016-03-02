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

    def assertNotAllowed(self, endpoint, disallowed=None, allowed=None):
        methods = ["POST", "PUT", "GET", "PATCH", "DELETE"]
        if allowed:
            disallowed = [m for m in methods if m not in allowed]

        for action in disallowed:
            if action == "POST":
                res = self.app.post(endpoint)
            if action == "PUT":
                res = self.app.put(endpoint)
            if action == "DELETE":
                res = self.app.delete(endpoint)
            if action == "GET":
                res = self.app.get(endpoint)
            if action == "PATCH":
                res = self.app.patch(endpoint)

            if res.status_code != 405:
                raise AssertionError(
                    "Expected 405 status code for %s action. Got %s."
                    % (action, res.status_code)
                )
