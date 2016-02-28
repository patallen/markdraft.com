import unittest

from models import User, db
from api.auth import jwt


class TestJWTTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(username="testuser", password="test")
        db.session.flush()

    def test_generate_claims(self):
        claims = jwt.generate_claims(dict(
            username=self.user.username,
            user_id=self.user.id,
        ))
        self.assertIsNotNone(claims.get('iat'))
        self.assertIsNotNone(claims.get('exp'))
        self.assertEqual(claims.get('username'), self.user.username)

    def test_create_token_for_user(self):
        token = jwt.create_token_for_user(self.user)
        self.assertGreater(len(token), 20)

    def test_verify_token(self):
        token = jwt.create_token_for_user(self.user)
        payload = jwt.verify_token(token)
        self.assertTrue(payload)
        self.assertEqual(payload.get('first_name'), 'testuser')
        self.assertFalse(jwt.verify_token("kdsjfldkfjkdajlf"))
