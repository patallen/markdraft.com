import json

from data.models import User, Document, Tag
from tests import BaseTestCase


class UsersViewsTestCase(BaseTestCase):
    def setUp(self):
        super(UsersViewsTestCase, self).setUp()
        self.user_dict = {
            "email": "testacct@testing.com",
            "username": "testing",
            "password1": "testtest",
            "password2": "testtest",
            "first_name": "testy_user",
            "last_name": "McUser"
        }

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
        res = self.app.post(
            '/auth/register',
            data=json.dumps(self.user_dict),
            headers=self.headers
        )
        self.assertStatus200(res)
        self.assertIsNotNone(User.query.filter_by(username="testing").first())

    def test_auth_nonmatching_pw_registration(self):
        self.user_dict['password2'] = "nomatch"
        res = self.app.post(
            '/auth/register',
            data=json.dumps(self.user_dict),
            headers=self.headers
        )
        self.assertStatus(res, 422)
        self.assertTrue("do not match" in res.data)

    def test_auth_email_taken_registration(self):
        self.user_dict['email'] = self.default_user.email
        res = self.app.post(
            '/auth/register',
            data=json.dumps(self.user_dict), headers=self.headers
        )
        self.assertStatus(res, 409)
        self.assertTrue("not available" in res.data)

    def test_auth_correct_login(self):
        req = json.dumps({
            "username": "testuser",
            "password": "123abc"
        })
        res = self.app.post('/auth/login', data=req, headers=self.headers)
        self.assertStatus200(res)
        results = json.loads(res.data).get('results')
        self.assertAllIn(results.keys(), ['access_token'])

    def test_auth_incorrect_login(self):
        req = json.dumps({
            "username": "testuser",
            "password": "wrongpassword"
        })
        res = self.app.post(
            '/auth/login',
            data=req,
            headers=self.headers
        )
        self.assertStatus(res, 401)
        self.assertTrue('Trouble authenticating' in res.data)

    def test_get_user_tags(self):
        get = self.app.get('/users/1/tags', headers=self.headers)
        self.assertStatus(get, 200)
        results = json.loads(get.data).get('results')
        self.assertEqual(len(results), 1)
        self.assertNotAllowed("/users/1/tags", allowed=['GET'])


class DocumentsViewsTestCase(BaseTestCase):
    def test_create_document(self):
        self.assertNotAllowed("/documents", allowed=['POST'])
        req = json.dumps({
            "title": "TEST DOC",
        })
        res = self.app.post("/documents", data=req, headers=self.headers)

        self.assertStatus(res, 201)
        self.assertIsNotNone(Document.query.filter_by(title="TEST DOC").all())

    def test_get_document(self):
        res = self.app.get('/documents/1')
        results = json.loads(res.data).get('results')
        self.assertStatus200(res)
        self.assertAllIn(results, ['created_at', 'title', 'updated_at', 'id'])
        self.assertEqual(results['title'], "This is a Test Title")

    def test_edit_document(self):
        req = json.dumps({"title": "this is a new title"})
        res = self.app.put('/documents/1', data=req, headers=self.headers)
        self.assertStatus200(res)
        doc = Document.query.get(1)
        self.assertEqual(doc.title, "this is a new title")

    def test_delete_document(self):
        res = self.app.delete('/documents/1', headers=self.headers)
        self.assertStatus200(res)
        doc = Document.query.get(1)
        self.assertIsNone(doc)


class TagsViewsTestCase(BaseTestCase):
    def setUp(self):
        super(TagsViewsTestCase, self).setUp()

    def test_create_tag(self):
        user_id = self.default_user.id
        tag_dict = json.dumps({"title": "TEST TAG"})
        res = self.app.post('/tags', data=tag_dict, headers=self.headers)

        tag = Tag.query.filter_by(title="TEST TAG").first()

        self.assertStatus(res, 201)
        self.assertIsNotNone(tag)
        self.assertEqual(user_id, tag.user_id)

    def test_get_tag(self):
        res = self.app.get('/tags/1', headers=self.headers)
        self.assertStatus200(res)
