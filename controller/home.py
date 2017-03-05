# coding=utf-8
from tornado import gen

from base import BaseHandler
from admin_article import ArticleAndCommentsFlush
from model.pager import Pager
from model.constants import Constants
from model.search_params.article_params import ArticleSearchParams
from model.search_params.comment_params import CommentSearchParams
from service.user_service import UserService
from service.article_service import ArticleService
from service.comment_service import CommentService


class HomeHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        pager = Pager(self)
        article_search_params = ArticleSearchParams(self)
        article_search_params.show_article_type = True
        article_search_params.show_source = True
        article_search_params.show_summary = True
        article_search_params.show_comments_count = True
        pager = yield self.async_do(ArticleService.page_articles, self.db, pager, article_search_params)
        self.render("index.html", base_url=self.reverse_url('index'),
                    pager=pager, article_search_params=article_search_params)


class ArticleHandler(BaseHandler):
    @gen.coroutine
    def get(self, article_id):
        article = yield self.async_do(ArticleService.get_article_all, self.db, article_id, True)
        comments_pager = Pager(self)
        comment_search_params = CommentSearchParams(self)
        comment_search_params.article_id = article_id
        comments_pager = yield self.async_do(CommentService.page_comments, self.db, comments_pager, comment_search_params)
        self.render("article_detials.html", article=article, comments_pager=comments_pager)


class ArticleCommentHandler(BaseHandler, ArticleAndCommentsFlush):
    @gen.coroutine
    def post(self, article_id):
        comment = dict(
            content=self.get_argument('content'),
            author_name=self.get_argument('author_name'),
            author_email=self.get_argument('author_email'),
            article_id=article_id,
            comment_type=self.get_argument('comment_type', None),
            rank=Constants.COMMENT_RANK_ADMIN if self.current_user else Constants.COMMENT_RANK_NORMAL,
            reply_to_id=self.get_argument('reply_to_id', None),
            reply_to_floor=self.get_argument('reply_to_floor', None),
        )
        comment_saved = yield self.async_do(CommentService.add_comment, self.db, article_id, comment)
        if comment_saved:
            yield self.flush_comments_cache(Constants.FLUSH_COMMENT_ACTION_ADD, comment_saved)
            self.add_message('success', u'评论成功')
        else:
            self.add_message('danger', u'评论失败')
        self.redirect(self.reverse_url('article', article_id)+"?pageNo=-1#comments")


class ArticleTypeHandler(BaseHandler):
    @gen.coroutine
    def get(self, type_id):
        pager = Pager(self)
        article_search_params = ArticleSearchParams(self)
        article_search_params.show_article_type=True
        article_search_params.show_source=True
        article_search_params.show_summary=True
        article_search_params.show_comments_count = True
        article_search_params.articleType_id = type_id
        pager = yield self.async_do(ArticleService.page_articles, self.db, pager, article_search_params)
        self.render("index.html", base_url=self.reverse_url('articleType', type_id),
                    pager=pager, article_search_params=article_search_params)


class articleSourceHandler(BaseHandler):
    @gen.coroutine
    def get(self, source_id):
        pager = Pager(self)
        article_search_params = ArticleSearchParams(self)
        article_search_params.show_article_type=True
        article_search_params.show_source=True
        article_search_params.show_summary=True
        article_search_params.show_comments_count = True
        article_search_params.source_id = source_id
        pager = yield self.async_do(ArticleService.page_articles, self.db, pager, article_search_params)
        self.render("index.html", base_url=self.reverse_url('articleSource', source_id),
                    pager=pager, article_search_params=article_search_params)


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


