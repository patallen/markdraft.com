from flask import Response

from . import BaseTestCase
from models import User


class TestingTestCase(BaseTestCase):
    def test_test_user_in_db(self):
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)

    def test_default_user(self):
        self.assertIsNotNone(self.default_user)
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(self.default_user, user)

    def test_assertAllIn(self):
        test_list = ['a', 'b', 'c']
        self.assertTrue(self.assertAllIn(test_list, ['a', 'b', 'c']))

        with self.assertRaises(AssertionError):
            self.assertAllIn(test_list, ['d'])

    def test_status_assertions(self):
        response = Response()
        response.status_code = 401

        with self.assertRaises(AssertionError):
            self.assertStatus(response, 400)
        with self.assertRaises(AssertionError):
            self.assertStatus200(response)

    def test_assertNotAllowed(self):
        with self.assertRaises(AssertionError):
            self.assertNotAllowed('/documents', allowed=['PUT'])
        with self.assertRaises(ValueError):
            self.assertNotAllowed('/documents', disallowed=['JD'])
