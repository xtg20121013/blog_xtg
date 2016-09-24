# coding=utf-8
import tornado.web
from tornado import gen
from extends.session_tornadis import Session


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = None
        self.db_session = None
        self.thread_executor = self.application.thread_executor

    @gen.coroutine
    def init_session(self):
        if not self.session:
            self.session = Session(self)
            yield self.session.init_fetch()

    @gen.coroutine
    def save_session(self):
        yield self.session.save()

    def get_current_user(self):
        yield self.init_session()
        if "user" in self.session:
            return self.session["user"]

    @property
    def db(self):
        if not self.db_session:
            self.db_session = self.application.db_pool()
        return self.db_session

    def on_finish(self):
        pass
