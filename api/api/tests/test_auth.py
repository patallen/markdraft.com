from mock import Mock

from api.auth import jwt
from tests import BaseTestCase


class TestJWTTestCase(BaseTestCase):
    def setUp(self):
        super(TestJWTTestCase, self).setUp()
        self.agent = 'CHROMIUM 1.2.3.4.5'
        self.user_id = 1

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
        succ, payload = jwt.verify_token(good_token)
        self.assertTrue(succ)
        self.assertEqual(payload.get('first_name'), 'Test')
        succ, bad_payload = jwt.verify_token("lsdkjfdskjfs")
        self.assertFalse(succ)
        self.assertIn("tampered", bad_payload)

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
            self.assertEqual(401, res.status_code)

        with self.app.test_request_context(headers=nobearer_header):
            res = mock_fn()
            self.assertEqual(401, res.status_code)

        with self.app.test_request_context():
            res = mock_fn()
            self.assertEqual(401, res.status_code)
        good_header = {
            "Authorization": "Bearer %s" % token
        }
        with self.app.test_request_context(headers=good_header):
            res = mock_fn()
            self.assertEqual("success", res)

    def test_create_refresh_token(self):
        with self.assertRaises(ValueError):
            jwt.create_refresh_token(self.user_id, None)

    def test_generate_refresh_payload(self):
        should_equal = dict(u=self.user_id, a=self.agent)
        payload = jwt.generate_refresh_payload(self.user_id, self.agent)
        self.assertEqual(should_equal, payload)

    def test_verify_refresh_token(self):
        token = jwt.create_refresh_token(self.user_id, self.agent)
        bad_token = token[:len(token)-3]
        self.assertTrue(
            jwt.verify_refresh_token(token, self.user_id, self.agent)
        )
        self.assertFalse(
            jwt.verify_refresh_token(bad_token, self.user_id, self.agent)
        )
