import json

from models import User
from tests import BaseTestCase


class UsersTestCase(BaseTestCase):
    def test_users_get(self):
        res = self.app.get('/users')
        self.assertStatus200(res)
        results = json.loads(res.data).get('results')
        self.assertEqual(len(results), 1)
        self.assertNotAllowed("/users", allowed=["GET"])

    def test_users_documents(self):
        get = self.app.get('/users/1/documents')
        self.assertStatus(get, 200)
        results = json.loads(get.data).get('results')
        self.assertEqual(len(results), 1)
        self.assertNotAllowed("/users/1/documents", allowed=['GET'])

    def test_auth_registration(self):
        req = {
            "email": "testacct@testing.com",
            "username": "testing",
            "password1": "testtest",
            "password2": "testtest",
            "first_name": "testy_user",
            "last_name": "McUser"
        }
        res = self.app.post(
            '/auth/register',
            data=json.dumps(req),
            headers=[('Content-Type', 'application/json')]
        )
        self.assertStatus200(res)
        self.assertIsNotNone(User.query.filter_by(username="testing").first())

    def test_auth_login(self):
        req = json.dumps({
            "username": "testuser",
            "password": "123abc"
        })
        res = self.app.post(
            '/auth/login',
            data=req,
            headers=[('Content-Type', 'application/json')]
        )
        self.assertStatus200(res)
        results = json.loads(res.data).get('results')
        self.assertAllIn(results.keys(), ['access_token'])
