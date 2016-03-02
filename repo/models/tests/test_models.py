from tests import BaseTestCase

from models import Document, db


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
