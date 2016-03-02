import unittest

from models import Document, User, db
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
        document = Document(
            title="This is a Test Title",
            user_id=self.default_user.id
        )
        document.save()
        self.default_document = document

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

        if allowed is not None:
            disallowed = [m for m in methods if m not in allowed]

        for action in disallowed:
            res = self.action(endpoint, action)

            if action.upper() not in methods:
                raise ValueError("%s is not an accepted method." % action)

            if res.status_code != 405:
                raise AssertionError(
                    "Expected 405 status code for %s action. Got %s."
                    % (action, res.status_code)
                )

    def action(self, endpoint, method, **kwargs):
        kwargs['method'] = method.upper()
        return self.app.open(endpoint, **kwargs)
