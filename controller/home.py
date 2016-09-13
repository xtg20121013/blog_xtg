# coding=utf-8
import tornado.web
from tornado import gen
from base import BaseHandler


class HomeHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        session = self.get_session()
        if 'st' not in session:
            st = 'hello world'
            session['st'] = st
            self.save_session()
        self.write(self.session['st'])
