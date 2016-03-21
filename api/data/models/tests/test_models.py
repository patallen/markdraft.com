from tests import BaseTestCase

from data.models import Document, User, Share, db


class BaseMixinTestCase(BaseTestCase):

    def test_update_attributes(self):
        self.default_document.update_attributes({"title": "BOOM"})
        self.default_document.save()
        self.assertEqual(self.default_document.title, "BOOM")

    def test_get(self):
        title = "This is a Test Title"
        self.assertEqual(self.default_document.get('title'), title)

    def test_to_dict(self):
        dic = self.default_document.to_dict()
        self.assertAllIn(
            dic.keys(),
            ["title", "created_at",
             "updated_at", "id"]
        )

    def test_to_dict_exclude(self):
        dic = self.default_document.to_dict(exclude="id")
        self.assertTrue("id" not in dic.keys())

    def test_to_dict_include(self):
        dic = self.default_user.to_dict(include="_password")
        self.assertTrue("_password" in dic.keys())

    def test_delete(self):
        self.default_document.delete()
        self.assertIsNone(Document.query.first())

    def test_create(self):
        User.create({
            "username": "testy",
            "email": "testy@test.com",
            "password": "testypass"
        })
        db.session.flush()
        db.session.expire_all()
        get = User.query.filter_by(username="testy").first()
        self.assertIsNotNone(get)
        self.assertEqual(get.email, "testy@test.com")


class DocumentModelTestCase(BaseTestCase):
    def setUp(self):
        super(DocumentModelTestCase, self).setUp()
        self.user2 = User.create({
            "username": "user2",
            "email": "user2@user.com",
            "password": "user2",
        })
        Share.create_or_update(self.user2, self.default_document, read=True)
        self.random_doc = Document.create({"title": "random document"})

    def test_user_is_owner(self):
        self.assertTrue(self.default_document.user_is_owner(self.default_user))
        self.assertFalse(self.default_document.user_is_owner(self.user2))

    def test_user_has_access(self):
        self.assertTrue(
            self.default_document.user_has_access(self.default_user))
        self.assertTrue(
            self.default_document.user_has_access(self.user2, 'read'))
        self.assertFalse(
            self.default_document.user_has_access(self.user2, 'write'))
        self.assertFalse(
            self.random_doc.user_has_access(self.user2, 'read'))


class UserModelTestCase(BaseTestCase):
    def test_password(self):
        first_pass = self.default_user.password
        self.assertIsNotNone(first_pass)
        self.assertNotEqual(first_pass, "123abc")
        self.default_user.password = "iLoVeCaNdy"
        self.assertNotEqual(first_pass, self.default_user.password)

    def test_authenticate(self):
        self.assertTrue(
            self.default_user.authenticate("123abc")
        )
        self.assertFalse(
            self.default_user.authenticate("NOTITNOTIT")
        )

    def test_active_and_admin(self):
        self.assertTrue(self.default_user.is_active)
        self.assertTrue(self.default_user.is_admin)
        self.default_user.update_attributes({"_admin": False})
        self.assertFalse(self.default_user.is_admin)

    def test_owns_document(self):
        doc = Document.query.first()
        self.assertTrue(self.default_user.owns_document(doc))
        new_doc = Document.create({"title": "random document"})
        self.assertFalse(self.default_user.owns_document(new_doc))


class SharesTestCase(BaseTestCase):
    def setUp(self):
        super(SharesTestCase, self).setUp()
        self.user2 = User.create(dict(
            username="user2",
            password="pwpwpw",
            email="user2@gmail.com"
        ))
        Share.create_or_update(self.user2, self.default_document)

    def test_create_or_update_share(self):
        Share.create_or_update(self.user2, self.default_document)
        Share.create_or_update(
            self.user2, self.default_document, write=True
        )
        self.assertTrue(
            self.default_document.user_has_access(self.user2, 'write')
        )

    def test_get_share(self):
        with self.assertRaises(ValueError):
            Share.get_share(user=self.default_user)

        self.assertIsNotNone(
            Share.get_share(self.user2, self.default_document)
        )

    def test_shares_for_user_query(self):
        query = Share.shares_for_user_query(user=self.user2)
        self.assertIsNotNone(query.all())
        self.assertIsNone(Share.shares_for_user_query())

    def test_shares_for_user(self):
        readable = Share.shares_for_user(user=self.user2, read=True)
        self.assertGreater(len(readable), 0)

        writable = Share.shares_for_user(user=self.user2, write=True)
        self.assertEqual(len(writable), 0)
