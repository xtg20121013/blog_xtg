# coding=utf-8
from tornado.gen import coroutine
from tornado.web import authenticated
from service.article_type_service import ArticleTypeService
from base import BaseHandler


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

    # @coroutine
    # def post(self, *require):
    #     if require:
    #         if len(require) == 1:
    #             if require[0] == 'add':
    #                 yield self.add_post()
    #         elif len(require) == 2:
    #             article_type_id = require[0]
    #             action = require[1]
    #             if action == 'update':
    #                 yield self.update_post(article_type_id)

    @coroutine
    @authenticated
    def submit_get(self):
        article_types = yield self.async_do(ArticleTypeService.list_simple, self.db)
        self.render("admin/submit_articles.html", article_types=article_types)
