import unittest
import time

from fakeredis import FakeStrictRedis

from marklib.redis_store import RedisStore


class RedisStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.prefix = 'test'
        self.redis_store = RedisStore(store=FakeStrictRedis, name=self.prefix)

    def tearDown(self):
        self.redis_store.store.flushall()

    def test_set_method(self):
        self.redis_store.set('a', 'valuevaluevalue')
        self.assertEqual(
            self.redis_store.store.get('{}|a'.format(self.prefix)),
            'valuevaluevalue'
        )
        self.redis_store.set('willexpire', 'value', expire=.1)
        time.sleep(.2)
        self.assertIsNone(self.redis_store.get('willexpire'))

    def test_get_method(self):
        self.redis_store.store.set('{}|key'.format(self.prefix), 'value')
        self.assertEqual(
            self.redis_store.get('key'),
            'value'
        )

    def test_name_set(self):
        self.assertEqual(self.redis_store.name, self.prefix+'|')

    def test_delete_method(self):
        self.redis_store.set('key', 'value')
        self.assertGreater(len(self.redis_store.store.keys()), 0)

        self.redis_store.delete('key')
        self.assertEqual(len(self.redis_store.store.keys()), 0)

    def test_keys_method(self):
        self.redis_store.set('key1', 'value')
        self.redis_store.set('key2', 'value')
        keys = ['test|key2', 'test|key1']
        self.assertEqual(self.redis_store.keys(), keys)
