from redis import StrictRedis


class RedisStore(object):

    DEFAULT_STORE = StrictRedis
    DEFAULT_NAME = 'store'
    DEFAULT_EXPIRY = None

    def __init__(
        self,
        store=None,
        name=None,
        default_expiry=None
    ):
        self.store = store
        if self.store is None:
            self.store = self.DEFAULT_STORE()

        self.name = name or self.DEFAULT_NAME
        if self.name[-1] != '|':
            self.name = self.name + '|'

        self.default_expiry = default_expiry or self.DEFAULT_EXPIRY

    def set(self, key, data, expire=None):
        if expire is not False:
            expire = expire or self.default_expiry

        self.store.set(self.name+key, data)

        if expire:
            self.store.expire(self.name+key, expire)

    def get(self, key):
        return self.store.get(self.name+key)

    def delete(self, *keys):
        keys = map(lambda s: '%s%s' % (self.name, s), keys)
        return self.store.delete(*keys) > 0

    def keys(self):
        return self.store.keys('%s*' % self.name)
