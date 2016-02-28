import unittest

from marklib import helpers


class MarklibHelpersTestCase(unittest.TestCase):
    def test_random_int(self):
        random = helpers.random_int(low=1, high=1000)
        self.assertLess(random, 1001)
        self.assertGreater(random, 0)
