# coding: utf-8
import logging

import tornadis
import tornado.gen

logger = logging.getLogger(__name__)


class CacheManager(object):
    def __init__(self, options):
        self.connection_pool = None
        self.options = options
        self.client = None

    def get_connection_pool(self):
        if not self.connection_pool:
            self.connection_pool = tornadis.ClientPool(host=self.options['host'],port=self.options['port'],
                                                       password=self.options['password'], db=self.options['db_no'],
                                                       max_size=self.options['max_connections'])
        return self.connection_pool

    @tornado.gen.coroutine
    def get_redis_client(self):
        connection_pool = self.get_connection_pool()
        with (yield connection_pool.connected_client()) as client:
            if isinstance(client, tornadis.TornadisException):
                logger.error(client.message)
            else:
                raise tornado.gen.Return(client)

    @tornado.gen.coroutine
    def fetch_client(self):
        self.client = yield self.get_redis_client()

    @tornado.gen.coroutine
    def call(self, *args, **kwargs):
        yield self.fetch_client()
        if self.client:
            reply = yield self.client.call(*args, **kwargs)
            if isinstance(reply, tornadis.TornadisException):
                logger.error(reply.message)
            else:
                raise tornado.gen.Return(reply)