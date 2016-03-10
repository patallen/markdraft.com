import unittest

from api.app import create_app
from api import config
from api.auth import jwt
from data.models import Document, Tag, User, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app = create_app(config.Testing)
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()
        tag = Tag(title="TAGGY")
        self.default_user = User(
            username="testuser",
            password="123abc",
            first_name="Test",
            last_name="User"
        )
        self.default_user.tags.append(tag)
        document = Document(
            title="This is a Test Title",
            user_id=self.default_user.id
        )
        self.default_document = document

        token = jwt.create_token_for_user(self.default_user)
        self.headers = [
            ('Content-Type', 'application/json'),
            ('Authorization', 'Bearer %s' % token)
        ]
        db.session.add(document)
        db.session.add(self.default_user)
        db.session.add(tag)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def assertAllIn(self, theirs, ours):
        for val in ours:
            if val not in theirs:
                raise AssertionError("Expected %s in list." % (val,))
        return True

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
        return self.client.open(endpoint, **kwargs)
