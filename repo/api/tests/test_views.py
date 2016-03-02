from tests import BaseTestCase
import json


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
