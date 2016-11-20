# coding=utf-8
import logging
import tornado.gen
from extends.pub_sub_tornadis import PubSubTornadis

logger = logging.getLogger(__name__)


class PubSubService(PubSubTornadis):

    @tornado.gen.coroutine
    def do_msg(self, msg):
        print msg
        logger.info("shoudaole")