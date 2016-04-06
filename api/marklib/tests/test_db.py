import unittest

from tests import BaseTestCase
from marklib.db import filters
from data.models import Document


class FiltersTestCase(BaseTestCase):
    def setUp(self):
        super(FiltersTestCase, self).setUp()
        documents = [
            {
                "title": "Title 1",
                "body": "blank"
            },
            {
                "title": "Title 2",
                "body": "blank"
            },
            {
                "title": "Title 3",
                "body": "blank"
            },
        ]
        for doc in documents:
            d = Document(
                title=doc.get('title'),
                body=doc.get('body')
            )
            self.db.session.add(d)
        self.db.session.commit()

    def test_values_filter(self):
        query = Document.query

        docs = filters.values_filter(query, Document.title, ['Title 1'])
        self.assertEqual(docs.count(), 1)

        docs = filters.values_filter(query, Document.title, 'Title 1')
        self.assertEqual(docs.count(), 1)

        docs = filters.values_filter(query, Document.title, 'Title 10')
        self.assertEqual(docs.count(), 0)
