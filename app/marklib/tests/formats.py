import unittest
from datetime import datetime

from marklib.formats import dates


class TestTimestampTestCase(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(1990, 2, 25, 0, 1, 0, 0)

    def test_timestamp_type(self):
        ts = dates.timestamp(self.dt)
        self.assertIsInstance(ts, int)

    def test_timestamp_values(self):
        ts = dates.timestamp(self.dt)
        self.assertGreater(ts, 0)
        self.assertEqual(ts, 635922060)
