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

    def test_contains_string_filter(self):
        query = Document.query

        docs = filters.contains_string(query, Document.title, 'Title')
        self.assertEqual(docs.count(), 4)

        docs = filters.contains_string(query, Document.title, 'title')
        self.assertEqual(docs.count(), 4)

        docs = filters.contains_string(query, Document.title, 'zzzzzzz')
        self.assertEqual(docs.count(), 0)

    def test_limit_and_offset(self):
        limit = 2
        query = Document.query
        docs = filters.limit_and_offset(query, rows=limit)
        self.assertEqual(docs.count(), 2)

    def test_sort_query(self):
        query = Document.query
        sort_string = "title desc"
        doc_query = filters.sort_query(query, Document, sort_string)
        self.assertEqual(doc_query[0].title, 'Title 3')
