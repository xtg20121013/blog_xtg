# coding=utf-8
import tornado.web
from tornado import gen
from extends.session_tornadis import Session
from config import session_keys
from model.logined_user import LoginUser


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = None
        self.db_session = None
        self.messages = None
        self.thread_executor = self.application.thread_executor

    @gen.coroutine
    def prepare(self):
        yield self.init_session()
        if session_keys['login_user'] in self.session:
            self.current_user = LoginUser(self.session[session_keys['login_user']])

    @gen.coroutine
    def init_session(self):
        if not self.session:
            self.session = Session(self)
            yield self.session.init_fetch()

    @gen.coroutine
    def save_session(self):
        yield self.session.save()

    @property
    def db(self):
        if not self.db_session:
            self.db_session = self.application.db_pool()
        return self.db_session

    # category:['success','info', 'warning', 'danger']
    def add_message(self, category, message):
        item = {'category':category, 'message':message}
        if not self.messages:
            self.messages = [item]
        else:
            self.messages.append(item)

    def read_messages(self):
        all_messages = self.messages
        self.messages = None
        return all_messages

    def on_finish(self):
        if self.db_session:
            self.db_session.close()
            print "db_info:", self.application.db_pool.kw['bind'].pool.status()

