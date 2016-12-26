# coding=utf-8
from tornado.web import authenticated
from tornado.gen import coroutine
from base import BaseHandler
from model.pager import Pager
from model.search_params.menu_params import MenuSearchParams
from service.menu_service import MenuService
from service.init_service import SiteCacheService


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
        if require:
            if len(require) == 2:
                menu_id = require[0]
                action = require[1]
                if action == 'sort-up':
                    pass
                elif action == 'sort-down':
                    pass
        else:
            yield self.page_get()

    @coroutine
    def post(self, *require):
        if require:
            if len(require) == 1:
                if require[0] == 'add':
                    yield self.add_post()
            # elif len(require) == 2:
            #     plugin_id = require[0]
            #     action = require[1]
            #     if action == 'edit':
            #         yield self.edit_post(plugin_id)


    @coroutine
    @authenticated
    def page_get(self):
        pager = Pager(self)
        menu_search_params = MenuSearchParams(self)
        pager = yield self.async_do(MenuService.page_menus, self.db, pager, menu_search_params)
        self.render("admin/manage_articleTypes_nav.html", pager=pager)

    @coroutine
    @authenticated
    def add_post(self):
        menu = dict(name=self.get_argument('name'),)
        menu_saved = yield self.async_do(MenuService.add_menu, self.db, menu)
        if menu_saved and menu_saved.id:
            yield self.flush_menus()
            self.add_message('success', u'保存成功!')
        else:
            self.add_message('danger', u'保存失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

    @coroutine
    def flush_menus(self, menus=None):
        if menus is None:
            menus = yield self.async_do(MenuService.list_menus, self.db, show_types=True)
        yield SiteCacheService.update_menus(self.cache_manager, menus,
                                            is_pub_all=True, pubsub_manager=self.pubsub_manager)
