# coding=utf-8
from base import BaseHandler
from tornado.gen import coroutine
from tornado.web import authenticated
from service.user_service import UserService


class AdminAccountHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("admin/admin_account.html")

    @coroutine
    def post(self, require):
        if require == "edit-user-info":
            yield self.edit_user_info()
        elif require == "change-password":
            yield self.change_password()

    @authenticated
    @coroutine
    def edit_user_info(self):
        user_info = {"username": self.get_argument("username"), "email": self.get_argument("email")}
        user = yield self.async_do(UserService.update_user_info, self.db, self.current_user.name,
                                   self.get_argument("password"), user_info)
        if user:
            self.save_login_user(user)
            self.add_message('success', u'修改用户信息成功!')

        else:
            self.add_message('danger', u'修改用户信息失败！密码不正确!')
        self.redirect(self.reverse_url("admin.account"))

    @authenticated
    @coroutine
    def change_password(self):
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("password")
        count = yield self.async_do(UserService.update_password, self.db, self.current_user.name,
                                    old_password, new_password)
        if count > 0:
            self.add_message('success', u'修改密码成功!')
        else:
            self.add_message('danger', u'修改密码失败！')
        self.redirect(self.reverse_url("admin.account"))


class AdminHelpHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render('admin/help_page.html')