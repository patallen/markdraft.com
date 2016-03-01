from tests import BaseTestCase

from models import Document, db


class BaseMixinTestCase(BaseTestCase):
    def setUp(self):
        super(BaseMixinTestCase, self).setUp()
        doc = Document(
            title="This is a Test Title",
            user=self.default_user
        )
        doc.save()
        self.doc = doc

    def test_update_attributes(self):
        self.doc.update_attributes({"title": "BOOM"})
        self.doc.save()
        self.assertEqual(self.doc.title, "BOOM")

    def test_get(self):
        title = "This is a Test Title"
        self.assertEqual(self.doc.get('title'), title)

    def test_to_dict(self):
        dic = self.doc.to_dict()
        self.assertAllIn(
            dic.keys(),
            ["title", "created_at",
             "updated_at", "id"]
        )

    def test_to_dict_exclude(self):
        dic = self.doc.to_dict(exclude="id")
        self.assertTrue("id" not in dic.keys())

    def test_to_dict_include(self):
        dic = self.default_user.to_dict(include="_password")
        self.assertTrue("_password" in dic.keys())

    def test_delete(self):
        self.doc.delete()
        self.assertIsNone(Document.query.first())
