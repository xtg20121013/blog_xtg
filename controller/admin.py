# coding=utf-8
from base import BaseHandler
from tornado.web import authenticated


class AdminAccountHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("admin/admin_account.html")