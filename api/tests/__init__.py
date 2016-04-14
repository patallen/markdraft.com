import unittest

from api.app import create_app
from api import config
from api.auth import jwt
from data import db
from data.models import Document, Tag, User
from fakeredis import FakeStrictRedis
from marklib.redis_store import RedisStore


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app = create_app(config.Testing)
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        self.db = db
        self.db.drop_all()
        self.db.create_all()
        self.user = dict(
            username="testuser",
            password="123abc",
            first_name="Test",
            last_name="User",
            _admin=True
        )
        self.document = dict(
            title="This is a Test Title",
            body="Body Body Body, likeasomebody"
        )
        self.tag = {"title": "TAGGY"}

        self.default_user = User.create(self.user)
        self.default_document = Document.create(self.document)
        self.default_document.user = self.default_user
        self.tag = Tag.create(self.tag)
        self.tag.user = self.default_user
        self.default_document.tags.append(self.tag)
        self.db.session.commit()
        self.redis_store = RedisStore(store=FakeStrictRedis, name='test')
        token = jwt.create_token_for_user(self.default_user)
        self.headers = [
            ('Content-Type', 'application/json'),
            ('Authorization', 'Bearer %s' % token)
        ]

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

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
