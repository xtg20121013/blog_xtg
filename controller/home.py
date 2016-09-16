# coding=utf-8
import tornado.web
from tornado import gen
from base import BaseHandler


class HomeHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        yield self.init_session()
        if 'st' not in self.session:
            st = 'hello world'
            self.session['st'] = st
            yield self.save_session()
            self.write(self.session['st'])
        self.write(self.request.remote_ip)
