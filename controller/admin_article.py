# coding=utf-8
from tornado.gen import coroutine
from tornado.web import authenticated

from base import BaseHandler
from config import session_keys
from model.models import Article
from service.article_service import ArticleService
from service.article_type_service import ArticleTypeService
from service.init_service import SiteCacheService


class AdminArticleHandler(BaseHandler):

    @coroutine
    def get(self, *require):
        if require:
            if len(require) == 1:
                action = require[0]
                if action == 'submit':
                    yield self.submit_get()
        #     if len(require) == 2:
        #         article_type_id = require[0]
        #         action = require[1]
        #         if action == 'delete':
        #             yield self.delete_get(article_type_id)
        # else:
        #     yield self.page_get()

    @coroutine
    def post(self, *require):
        if require:
            if len(require) == 1:
                if require[0] == 'submit':
                    yield self.submit_post()
            # elif len(require) == 2:
            #     article_type_id = require[0]
            #     action = require[1]
            #     if action == 'update':
            #         yield self.update_post(article_type_id)

    @coroutine
    @authenticated
    def submit_get(self):
        article_draft = self.session.pop(session_keys['article_draft'], None)
        article = None
        if article_draft:
            source_id = article_draft.get("source_id")
            type_id = article_draft.get("articleType_id")
            article = Article(source_id=int(source_id) if source_id else None,
                              title=article_draft.get("title"),
                              articleType_id=int(type_id) if type_id else None,
                              content=article_draft.get("content"),
                              summary=article_draft.get("summary"))
        article_types = yield self.async_do(ArticleTypeService.list_simple, self.db)
        self.render("admin/submit_articles.html", article_types=article_types, article=article)

    @coroutine
    @authenticated
    def submit_post(self):
        article = dict(
            source_id=self.get_argument("source_id"),
            title=self.get_argument("title"),
            articleType_id=self.get_argument("articleType_id"),
            content=self.get_argument("content"),
            summary=self.get_argument("summary"),
        )
        article_saved = yield self.async_do(ArticleService.add_article, self.db, article)
        if article_saved and article_saved.id:
            yield self.flush_article_count("add", article_saved)
            self.add_message('success', u'保存成功!')
            self.redirect(self.reverse_url('article', article_saved.id))
        else:
            self.add_message('danger', u'保存失败！')
            self.session[session_keys['article_draft']] = article
            self.redirect(self.reverse_url('admin.article.action', 'submit'))

    @coroutine
    def flush_article_count(self, action, article):
        yield SiteCacheService.update_article_action(self.cache_manager, action, article,
                                                     is_pub_all=True, pubsub_manager=self.pubsub_manager)
