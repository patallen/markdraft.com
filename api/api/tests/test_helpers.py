from tests import BaseTestCase
from data.models import User, Document
from api.helpers import filter_by_access


class APIHelpersTestCase(BaseTestCase):
    def test_filter_by_access(self):
        user = User.create(dict(
            username='testy',
            password='testy',
            email='testy@testy.co'
        ))
        Document.create(dict(title="title", body="d", user=user))
        available = filter_by_access(
            user,
            Document.query.all(),
        )
        self.assertEqual(len(available), 1)
