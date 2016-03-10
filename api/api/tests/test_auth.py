from mock import Mock

from api.auth import jwt
from tests import BaseTestCase


class TestJWTTestCase(BaseTestCase):
    def test_generate_claims(self):
        claims = jwt.generate_claims(dict(
            username=self.default_user.username,
            user_id=self.default_user.id,
        ))
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
        with self.app.test_request_context(headers=bad_header):
            res = mock_fn()
            self.assertEqual(401, res[1])

        with self.app.test_request_context(headers=nobearer_header):
            res = mock_fn()
            self.assertEqual(401, res[1])

        with self.app.test_request_context():
            res = mock_fn()
            self.assertEqual(401, res[1])
        good_header = {
            "Authorization": "Bearer %s" % token
        }
        with self.app.test_request_context(headers=good_header):
            res = mock_fn()
            self.assertEqual(res[0].status_code, 200)
