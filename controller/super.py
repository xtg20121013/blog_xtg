# coding=utf-8
from tornado import gen

from base import BaseHandler
from service.user_service import UserService


class SuperHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        user_count = yield self.async_do(UserService.get_count, self.db)
        if not user_count:
            self.render("super/init.html")
        else:
            self.write_error(404)

    @gen.coroutine
    def post(self):
        user = dict(
            email=self.get_argument('email'),
            username=self.get_argument('username'),
            password=self.get_argument('password'),
        )
        user_saved = yield self.async_do(UserService.save_user, self.db, user)
        if user_saved and user_saved.id:
            self.add_message('success', u'创建成功!')
            self.redirect(self.reverse_url('login'))
        else:
            self.add_message('danger', u'创建失败！')
            self.redirect(self.reverse_url('super.init'))
