# coding=utf-8
import tornado.web
from tornado import gen


class HomeHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        st = 'hello world'
        self.write(st)