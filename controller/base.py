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
        self.session_save_tag = False
        self.thread_executor = self.application.thread_executor
        self.cache_manager = self.application.cache_manager
        self.async_do = self.thread_executor.submit

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

    def save_session(self):
        self.session_save_tag = True
        self.session.generate_session_id()

    @property
    def db(self):
        if not self.db_session:
            self.db_session = self.application.db_pool()
        return self.db_session

    @property
    def pubsub_manager(self):
        return self.application.pubsub_manager

    def save_login_user(self, user):
        login_user = LoginUser(None)
        login_user['id'] = user.id
        login_user['name'] = user.username
        login_user['avatar'] = user.avatar
        login_user['email'] = user.email
        self.session[session_keys['login_user']] = login_user
        self.current_user = login_user
        self.save_session()

    def logout(self):
        if session_keys['login_user'] in self.session:
            del self.session[session_keys['login_user']]
            self.save_session()
        self.current_user = None

    def has_message(self):
        if session_keys['messages'] in self.session:
            return bool(self.session[session_keys['messages']])
        else:
            return False

    # category:['success','info', 'warning', 'danger']
    def add_message(self, category, message):
        item = {'category': category, 'message': message}
        if session_keys['messages'] in self.session and \
                isinstance(self.session[session_keys['messages']], dict):
            self.session[session_keys['messages']].append(item)
        else:
            self.session[session_keys['messages']] = [item]
        self.save_session()

    def read_messages(self):
        if session_keys['messages'] in self.session:
            all_messages = self.session.pop(session_keys['messages'], None)
            self.save_session()
            return all_messages
        return None

    @gen.coroutine
    def on_finish(self):
        if self.db_session:
            self.db_session.close()
            # print "db_info:", self.application.db_pool.kw['bind'].pool.status()
        if self.session is not None and self.session_save_tag:
            yield self.session.save()

