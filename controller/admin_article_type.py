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
                    yield self.sort_up_get(menu_id)
                elif action == 'sort-down':
                    yield self.sort_down_get(menu_id)
                elif action == 'delete':
                    yield self.delete_get(menu_id)
        else:
            yield self.page_get()

    @coroutine
    def post(self, *require):
        if require:
            if len(require) == 1:
                if require[0] == 'add':
                    yield self.add_post()
            elif len(require) == 2:
                menu_id = require[0]
                action = require[1]
                if action == 'update':
                    yield self.update_post(menu_id)

    @coroutine
    @authenticated
    def update_post(self, menu_id):
        menu = dict(name=self.get_argument('name'),)
        update_count = yield self.async_do(MenuService.update, self.db, menu_id, menu)
        if update_count:
            yield self.flush_menus()
            self.add_message('success', u'修改成功!')
        else:
            self.add_message('danger', u'保存失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def page_get(self):
        pager = Pager(self)
        menu_search_params = MenuSearchParams(self)
        pager = yield self.async_do(MenuService.page_menus, self.db, pager, menu_search_params)
        self.render("admin/manage_articleTypes_nav.html", pager=pager)

    @coroutine
    @authenticated
    def sort_up_get(self, menu_id):
        updated = yield self.async_do(MenuService.sort_up, self.db, menu_id)
        if updated:
            yield self.flush_menus()
            self.add_message('success', u'导航升序成功!')
        else:
            self.add_message('danger', u'操作失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def sort_down_get(self, menu_id):
        updated = yield self.async_do(MenuService.sort_down, self.db, menu_id)
        if updated:
            yield self.flush_menus()
            self.add_message('success', u'导航降序成功!')
        else:
            self.add_message('danger', u'操作失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def sort_up_get(self, menu_id):
        updated = yield self.async_do(MenuService.sort_up, self.db, menu_id)
        if updated:
            yield self.flush_menus()
            self.add_message('success', u'导航升序成功!')
        else:
            self.add_message('danger', u'操作失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def delete_get(self, menu_id):
        update_count = yield self.async_do(MenuService.delete, self.db, menu_id)
        if update_count:
            yield self.flush_menus()
            self.add_message('success', u'删除成功!')
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
