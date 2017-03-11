# coding=utf-8
import hashlib
import urllib

import datetime
import tornado.web
from tornado import gen
from tornado.escape import url_escape

from config import session_keys, config, cookie_keys
from extends.session_tornadis import Session
from model.logined_user import LoginUser
from service.init_service import SiteCacheService
from service.blog_view_service import BlogViewService


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = None
        self.db_session = None
        self.session_save_tag = False
        self.session_expire_time = 604800  # 7*24*60*60秒
        self.thread_executor = self.application.thread_executor
        self.cache_manager = self.application.cache_manager
        self.async_do = self.thread_executor.submit

    def login_url(self):
        return self.get_login_url()+"?next="+url_escape(self.request.uri)

    @gen.coroutine
    def prepare(self):
        yield self.init_session()
        if session_keys['login_user'] in self.session:
            self.current_user = LoginUser(self.session[session_keys['login_user']])
        yield self.add_pv_uv()

    #  增加pv，uv,
    #  每次调用pv+1, uv根据cookie每24小时只+1
    @gen.coroutine
    def add_pv_uv(self):
        add_pv = 1
        add_uv = 0
        date = datetime.date.today()
        last_view_day = self.get_secure_cookie(cookie_keys['uv_key_name'], None)
        if not last_view_day or int(last_view_day) != date.day:
            add_uv = 1
            self.set_secure_cookie(cookie_keys['uv_key_name'], str(date.day), 1)
        yield SiteCacheService.add_pv_uv(self.cache_manager, add_pv, add_uv,
                                         is_pub_all=True, pubsub_manager=self.pubsub_manager)
        yield self.async_do(BlogViewService.add_blog_view, self.db, add_pv, add_uv, date)

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
        login_user['avatar'] = self.get_gravatar_url(user.email)
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

    def write_json(self, json):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json)

    def write_error(self, status_code, **kwargs):
        if not config['debug']:
            if status_code == 403:
                self.render("403.html")
            elif status_code == 404 or 405:
                self.render("404.html")
            elif status_code == 500:
                self.render("500.html")
        if not self._finished:
            super(BaseHandler, self).write_error(status_code, **kwargs)

    def get_gravatar_url(self, email, default=None, size=40):
        body = {'s': str(size)}
        if default:
            body["d"] = default;
        elif config['default_avatar_url']:
            body["d"] = config['default_avatar_url']
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode(body)
        return gravatar_url

    @gen.coroutine
    def on_finish(self):
        if self.db_session:
            self.db_session.close()
            # print "db_info:", self.application.db_pool.kw['bind'].pool.status()
        if self.session is not None and self.session_save_tag:
            yield self.session.save(self.session_expire_time)

