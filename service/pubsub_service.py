# coding=utf-8
import logging
import tornado.gen
from extends.pub_sub_tornadis import PubSubTornadis
from init_service import SiteCacheService
from config import redis_pub_sub_channels

logger = logging.getLogger(__name__)


class PubSubService(PubSubTornadis):

    def __init__(self, redis_pub_sub_config, application, loop=None):
        super(PubSubService, self).__init__(redis_pub_sub_config, loop)
        self.application = application
        self.db_pool = self.application.db_pool
        self.cache_manager = self.application.cache_manager
        self.thread_executor = self.application.thread_executor
        self.thread_do = self.thread_executor.submit
        self._db_session = None

    @property
    def db(self):
        if not self._db_session:
            self._db_session = self.application.db_pool()
        return self._db_session

    @tornado.gen.coroutine
    def first_do_after_subscribed(self):
        yield SiteCacheService.query_all(self.cache_manager, self.thread_do, self.db)

    @tornado.gen.coroutine
    def do_msg(self, msgs):
        logger.info("收到redis消息: " + str(msgs))
        if len(msgs) >= 3:
            channel = msgs[1]
            core_msgs = msgs[2:]
            if channel == redis_pub_sub_channels['cache_message_channel']:
                yield SiteCacheService.update_by_sub_msg(core_msgs, self.cache_manager, self.thread_do, self.db)