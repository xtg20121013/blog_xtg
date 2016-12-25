# coding=utf-8
from tornado.web import authenticated
from tornado.gen import coroutine
from base import BaseHandler
from model.pager import Pager
from model.search_params.menu_params import MenuSearchParams
from service.menu_service import MenuService


class AdminArticleTypeHandler(BaseHandler):

    @coroutine
    def get(self, *require):
        if require:
            pass
        else:
            yield self.page_get()

    @coroutine
    @authenticated
    def page_get(self):
        pager = Pager(self)


class AdminArticleTypeNavHandler(BaseHandler):

    @coroutine
    def get(self, *require):
        if not require:
            yield self.page_get()

    @coroutine
    @authenticated
    def page_get(self):
        pager = Pager(self)
        menu_search_params = MenuSearchParams(self)
        pager = yield self.async_do(MenuService.page_menus, self.db, pager, menu_search_params)
        self.render("admin/manage_articleTypes_nav.html", pager=pager)
