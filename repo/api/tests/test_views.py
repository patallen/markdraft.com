from tests import BaseTestCase


class UsersTestCase(BaseTestCase):
    def test_users_get(self):
        res = self.app.get('/users')
        self.assertStatus200(res)
        self.assertNotAllowed("/users", allowed=["GET"])

    def test_users_documents(self):
        get = self.app.get('/users/1/documents')
        self.assertStatus(get, 200)
        self.assertNotAllowed("/users/1/documents", allowed=['GET'])
