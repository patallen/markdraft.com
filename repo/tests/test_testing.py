from . import BaseTestCase
from models import User


class TestingTestCase(BaseTestCase):
    def test_test_user_in_db(self):
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)

    def test_default_user(self):
        self.assertIsNotNone(self.default_user)
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(self.default_user, user)
