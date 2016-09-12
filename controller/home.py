# coding=utf-8
import tornado.web
from tornado import gen
from extends.session_redis import Session


class HomeHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = Session(self)

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        st = 'hello world'
        self.session['st'] = st
        self.session.save()
        self.write(self.session['st'])

    def on_finish(self):
        pass