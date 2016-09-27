# coding=utf-8
from tornado import web
from tornado import gen
from base import BaseHandler


class HomeHandler(BaseHandler):

    @web.authenticated
    @gen.coroutine
    def get(self):
        self.render("index.html")


class LoginHandler(BaseHandler):

    def get(self):
        self.render("auth/login.html")

    def post(self):
        self.write("hello")