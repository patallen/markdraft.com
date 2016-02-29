from marklib import helpers
from tests import BaseTestCase


class MarklibHelpersTestCase(BaseTestCase):
    def test_random_int(self):
        random = helpers.random_int(low=1, high=1000)
        self.assertLess(random, 1001)
        self.assertGreater(random, 0)
