from tests import BaseTestCase
from data.models import User, Document
from api.helpers import filter_by_access


class APIHelpersTestCase(BaseTestCase):
    def test_filter_by_access(self):
        user = User(
            username='testy',
            password='testy',
            email='testy@testy.co'
        )
        doc = Document(title="some title", body="dlksjflsk")
        user.documents.append(doc)
        user.save()
        available = filter_by_access(
            user,
            Document.query.all(),
        )
        self.assertEqual(len(available), 1)
