import unittest
from mock import Mock

from models import User
from api.auth import jwt
from api import app


class TestJWTTestCase(unittest.TestCase):
    def setUp(self):
        user = User.query.filter_by(username="testuser").first()
        if user is None:
            self.user = User(
                username="testuser",
                password="test",
                email="test@user.com",
            )
            self.user.save()
        else:
            self.user = user

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
        good_token = jwt.create_token_for_user(self.user)
        payload = jwt.verify_token(good_token)
        self.assertTrue(payload)
        self.assertEqual(payload.get('first_name'), 'testuser')
        self.assertFalse(jwt.verify_token("kdsjfldkfjkdajlf"))

        bad_token = jwt.jwt.dumps({"exp": 0})
        payload = jwt.verify_token(bad_token)
        self.assertFalse(payload)

    def test_require_jwt_decorator(self):
        mock = Mock(return_value="success")
        mock_fn = jwt.require_jwt(mock)
        bad_header = {
            "Authorization": "Bearer this-is-not-a-token"
        }
        nobearer_header = {
            "Authorization": "this-is-not-a-token"
        }
        token = jwt.create_token_for_user(self.user)
        good_header = {
            "Authorization": "Bearer %s" % token
        }
        with app.test_request_context(headers=bad_header):
            res = mock_fn()
            self.assertEqual(401, res[1])

        with app.test_request_context(headers=good_header):
            res = mock_fn()
            self.assertEqual("success", res)

        with app.test_request_context(headers=nobearer_header):
            res = mock_fn()
            self.assertEqual(401, res[1])

        with app.test_request_context():
            res = mock_fn()
            self.assertEqual(401, res[1])
