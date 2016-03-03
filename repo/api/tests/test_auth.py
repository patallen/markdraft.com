from mock import Mock

from api import app
from api.auth import jwt
from tests import BaseTestCase


class TestJWTTestCase(BaseTestCase):
    def test_generate_claims(self):
        claims = jwt.generate_claims(dict(
            username=self.default_user.username,
            user_id=self.default_user.id,
        ))
        self.assertIsNotNone(claims.get('iat'))
        self.assertIsNotNone(claims.get('exp'))
        self.assertEqual(claims.get('username'), self.default_user.username)

    def test_create_token_for_user(self):
        token = jwt.create_token_for_user(self.default_user)
        self.assertGreater(len(token), 20)

    def test_verify_token(self):
        good_token = jwt.create_token_for_user(self.default_user)
        payload = jwt.verify_token(good_token)
        self.assertTrue(payload)
        self.assertEqual(payload.get('first_name'), 'Test')
        self.assertFalse(jwt.verify_token("kdsjfldkfjkdajlf"))

        bad_token = jwt.jwt.dumps({"exp": 0})
        payload = jwt.verify_token(bad_token)
        self.assertFalse(payload)

    def test_require_jwt_decorator(self):
        mock = Mock(return_value="success")
        mock.__name__ = 'test_mock'
        mock_fn = jwt.require_jwt(mock)
        bad_header = {
            "Authorization": "Bearer this-is-not-a-token"
        }
        nobearer_header = {
            "Authorization": "this-is-not-a-token"
        }
        token = jwt.create_token_for_user(self.default_user)
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
