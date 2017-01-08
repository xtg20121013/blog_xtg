# coding=utf-8
from tornado.web import authenticated
from tornado.gen import coroutine
from base import BaseHandler
from model.pager import Pager
from model.search_params.menu_params import MenuSearchParams
from model.search_params.article_type_params import ArticleTypeSearchParams
from service.menu_service import MenuService
from service.init_service import SiteCacheService
from service.article_type_service import ArticleTypeService


class AdminArticleTypeBaseHandler(BaseHandler):
    @coroutine
    def flush_menus(self, menus=None, article_types_not_under_menu=None):
        if menus is None:
            menus = yield self.async_do(MenuService.list_menus, self.db, show_types=True)
        if article_types_not_under_menu is None:
            article_types_not_under_menu = yield \
                self.async_do(ArticleTypeService.list_article_types_not_under_menu, self.db)
        yield SiteCacheService.update_menus(self.cache_manager, menus, article_types_not_under_menu,
                                            is_pub_all=True, pubsub_manager=self.pubsub_manager)


class AdminArticleTypeHandler(AdminArticleTypeBaseHandler):

    @coroutine
    def get(self, *require):
        if require:
            if len(require) == 2:
                article_type_id = require[0]
                action = require[1]
                if action == 'delete':
                    yield self.delete_get(article_type_id)
        else:
            yield self.page_get()

    @coroutine
    def post(self, *require):
        if require:
            if len(require) == 1:
                if require[0] == 'add':
                    yield self.add_post()
            elif len(require) == 2:
                article_type_id = require[0]
                action = require[1]
                if action == 'update':
                    yield self.update_post(article_type_id)

    @coroutine
    @authenticated
    def page_get(self):
        pager = Pager(self)
        search_param = ArticleTypeSearchParams(self)
        search_param.show_setting = True
        search_param.show_articles_count = True
        pager = yield self.async_do(ArticleTypeService.page_article_types, self.db, pager, search_param)
        menus = yield self.async_do(MenuService.list_menus, self.db)
        self.render("admin/manage_articleTypes.html", pager=pager, menus=menus)

    @coroutine
    @authenticated
    def delete_get(self, article_type_id):
        update_count = yield self.async_do(ArticleTypeService.delete, self.db, article_type_id)
        if update_count:
            yield self.flush_menus()
            self.add_message('success', u'删除成功!')
        else:
            self.add_message('danger', u'删除失败！')
        redirect_url = self.reverse_url('admin.articleTypes')
        if self.request.query:
            redirect_url += "?" + self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def add_post(self):
        menu_id = int(self.get_argument("menu_id")) \
            if self.get_argument("menu_id") and self.get_argument("menu_id").isdigit() else None
        article_type = dict(
            name=self.get_argument("name"),
            setting_hide=self.get_argument("setting_hide") == 'true',
            introduction=self.get_argument("introduction"),
            menu_id=menu_id if menu_id > 0 else None,
        )
        added = yield self.async_do(ArticleTypeService.add_article_type, self.db, article_type)
        if added:
            yield self.flush_menus()
            self.add_message('success', u'保存成功!')
        else:
            self.add_message('danger', u'保存失败！')
        redirect_url = self.reverse_url('admin.articleTypes')
        if self.request.query:
            redirect_url += "?" + self.request.query
        self.redirect(redirect_url)

    @coroutine
    @authenticated
    def update_post(self, article_type_id):
        menu_id = int(self.get_argument("menu_id")) \
            if self.get_argument("menu_id") and self.get_argument("menu_id").isdigit() else None
        article_type = dict(
            id=article_type_id,
            name=self.get_argument("name"),
            setting_hide=self.get_argument("setting_hide") == 'true',
            introduction=self.get_argument("introduction"),
            menu_id=menu_id if menu_id > 0 else None,
        )
        updated = yield self.async_do(ArticleTypeService.update_article_type, self.db, article_type_id, article_type)
        if updated:
            yield self.flush_menus()
            self.add_message('success', u'修改成功!')
        else:
            self.add_message('danger', u'修改失败！')
        redirect_url = self.reverse_url('admin.articleTypes')
        if self.request.query:
            redirect_url += "?" + self.request.query
        self.redirect(redirect_url)


class AdminArticleTypeNavHandler(AdminArticleTypeBaseHandler):

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
    def add_post(self):
        menu = dict(name=self.get_argument('name'),)
        added = yield self.async_do(MenuService.add_menu, self.db, menu)
        if added:
            yield self.flush_menus()
            self.add_message('success', u'保存成功!')
        else:
            self.add_message('danger', u'保存失败！')
        redirect_url = self.reverse_url('admin.articleTypeNavs')
        if self.request.query:
            redirect_url += "?"+self.request.query
        self.redirect(redirect_url)

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
