# coding=utf-8
import tornado.web
from tornado import gen
from extends.session_tornadis import Session


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = None

    @gen.coroutine
    def init_session(self):
        if not self.session:
            self.session = Session(self)
            yield self.session.init_fetch()

    @gen.coroutine
    def save_session(self):
        yield self.session.save()

    @property
    def thread_executor(self):
        return self.application.thread_executor

    def on_finish(self):
        pass
