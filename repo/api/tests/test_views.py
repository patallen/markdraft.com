from tests import BaseTestCase


class UsersTestCase(BaseTestCase):
    def test_users_get(self):
        res = self.app.get('/users')
        self.assertStatus200(res)

    def test_users_not_get(self):
        post = self.app.post('/users')
        self.assertStatus(post, 405)
        put = self.app.put('/users')
        self.assertStatus(put, 405)
        patch = self.app.patch('/users')
        self.assertStatus(patch, 405)
        delete = self.app.delete('/users')
        self.assertStatus(delete, 405)

    def test_users_documents(self):
        get = self.app.get('/users/1/documents')
        self.assertStatus(get, 200)

    def test_users_documents_not_get(self):
        post = self.app.post('/users/1/documents')
        self.assertStatus(post, 405)
        put = self.app.put('/users/1/documents')
        self.assertStatus(put, 405)
        patch = self.app.patch('/users/1/documents')
        self.assertStatus(patch, 405)
        delete = self.app.delete('/users/1/documents')
        self.assertStatus(delete, 405)
