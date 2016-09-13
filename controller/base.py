# coding=utf-8
import tornado.web
from tornado import gen
from extends.session_redis import Session


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = None

    # @gen.coroutine
    def get_session(self):
        if not self.session:
            self.session = Session(self)
        return self.session

    # @gen.coroutine
    def save_session(self):
        self.session.save()

    def on_finish(self):
        pass
