# coding=utf-8
from tornado import gen

from base import BaseHandler
from model.pager import Pager
from model.search_params.article_params import ArticleSearchParams
from service.user_service import UserService
from service.article_service import ArticleService


class HomeHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        if self.request.query_arguments:
            # 取缓存
            pass
        pager = Pager(self)
        article_search_params = ArticleSearchParams(self)
        article_search_params.show_article_type=True
        article_search_params.show_source=True
        article_search_params.show_summary=True
        article_search_params.show_comments_count = True
        pager = yield self.async_do(ArticleService.page_articles, self.db, pager, article_search_params)
        self.render("index.html", pager=pager, article_search_params=article_search_params)


class LoginHandler(BaseHandler):

    def get(self):
        next_url = self.get_argument('next', '/')
        self.render("auth/login.html", next_url=next_url)

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '/')
        user = yield self.async_do(UserService.get_user, self.db, username)
        if user is not None and user.password == password:
            self.save_login_user(user)
            self.add_message('success', u'登陆成功！欢迎回来，{0}!'.format(username))
            self.redirect(next_url)
        else:
            self.add_message('danger', u'登陆失败！用户名或密码错误，请重新登陆。')
            self.get()


class LogoutHandler(BaseHandler):

    def get(self):
        self.logout()
        self.add_message('success', u'您已退出登陆。')
        self.redirect("/")


