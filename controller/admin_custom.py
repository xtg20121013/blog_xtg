# coding=utf-8
from base import BaseHandler
from tornado.gen import coroutine
from tornado.web import authenticated
from config import config
from model.pager import Pager
from model.search_params.plugin_params import PluginSearchParams
from service.custom_service import BlogInfoService
from service.init_service import SiteCacheService
from service.plugin_service import PluginService


class AdminCustomBlogInfoHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("admin/custom_blog_info.html", navbar_styles=config['navbar_styles'])

    @coroutine
    @authenticated
    def post(self):
        info = dict(title=self.get_argument("title"), signature=self.get_argument("signature"),
                    navbar=self.get_argument("navbar"),)
        blog_info = yield self.async_do(BlogInfoService.update_blog_info, self.db, info)
        if blog_info:
            #  更新本地及redis缓存，并发布消息通知其他节点更新
            yield self.flush_blog_info(blog_info)
            self.add_message('success', u'修改博客信息成功!')
        else:
            self.add_message('danger', u'修改失败！')
        self.redirect(self.reverse_url("admin.custom.blog_info"))

    @coroutine
    def flush_blog_info(self, blog_info):
        #  更新本地及redis缓存，并发布消息通知其他节点更新
        yield SiteCacheService.update_blog_info(self.cache_manager, blog_info,
                                                is_pub_all=True, pubsub_manager=self.pubsub_manager)


class AdminCustomBlogPluginHandler(BaseHandler):

    @coroutine
    def get(self, *require):
        if require:
            if len(require) == 1:
                if require[0] == 'add':
                    self.add_get()
            elif len(require) == 2:
                plugin_id = require[0]
                action = require[1]
                if action == 'sort-up':
                    yield self.sort_up_get(plugin_id)
                elif action == 'sort-down':
                    yield self.sort_down_get(plugin_id)
                elif action == 'disable':
                    yield self.set_disabled_get(plugin_id, True)
                elif action == 'enable':
                    yield self.set_disabled_get(plugin_id, False)
                elif action == 'delete':
                    yield self.delete_get(plugin_id)
        else:
            yield self.index_get()

    @coroutine
    def post(self, require):
        if require == 'add':
            yield self.add_post()

    @coroutine
    @authenticated
    def index_get(self):
        pager = Pager(self)
        plugin_search_params = PluginSearchParams(self)
        pager = yield self.async_do(PluginService.page_plugins, self.db, pager, plugin_search_params)
        self.render("admin/custom_blog_plugin.html", pager=pager)

    @authenticated
    def add_get(self):
        self.render("admin/blog_plugin_add.html")

    @coroutine
    @authenticated
    def sort_up_get(self, plugin_id):
        updated = yield self.async_do(PluginService.sort_up, self.db, plugin_id)
        if updated:
            yield self.flush_plugins()
            self.add_message('success', u'插件升序成功!')
        else:
            self.add_message('danger', u'操作失败！')
        self.redirect(self.reverse_url('admin.custom.blog_plugin')+"?"+self.request.query)

    @coroutine
    @authenticated
    def sort_down_get(self, plugin_id):
        updated = yield self.async_do(PluginService.sort_down, self.db, plugin_id)
        if updated:
            yield self.flush_plugins()
            self.add_message('success', u'插件降序成功!')
        else:
            self.add_message('danger', u'操作失败！')
        self.redirect(self.reverse_url('admin.custom.blog_plugin')+"?"+self.request.query)

    @coroutine
    @authenticated
    def set_disabled_get(self, plugin_id, disabled):
        updated_count = yield self.async_do(PluginService.update_disabled, self.db, plugin_id, disabled)
        if updated_count:
            yield self.flush_plugins()
            self.add_message('success', u'插件禁用成功!')
        else:
            self.add_message('danger', u'操作失败！')
        self.redirect(self.reverse_url('admin.custom.blog_plugin')+"?"+self.request.query)

    @coroutine
    @authenticated
    def delete_get(self, plugin_id):
        updated = yield self.async_do(PluginService.delete, self.db, plugin_id)
        if updated:
            yield self.flush_plugins()
            self.add_message('success', u'插件删除成功!')
        else:
            self.add_message('danger', u'操作失败！')
        self.redirect(self.reverse_url('admin.custom.blog_plugin')+"?"+self.request.query)

    @coroutine
    @authenticated
    def add_post(self):
        plugin = dict(title=self.get_argument('title'),note=self.get_argument('note'),
                      content=self.get_argument('content'),)
        plugin_saved = yield self.async_do(PluginService.save, self.db, plugin)
        if plugin_saved and plugin_saved.id:
            yield self.flush_plugins()
            self.add_message('success', u'保存成功!')
        else:
            self.add_message('danger', u'保存失败！')
        self.redirect(self.reverse_url('admin.custom.plugin.action', 'add'))

    @coroutine
    def flush_plugins(self, plugins=None):
        if plugins is None:
            plugins = yield self.async_do(PluginService.list_plugins, self.db)
        yield SiteCacheService.update_plugins(self.cache_manager, plugins,
                                              is_pub_all=True, pubsub_manager=self.pubsub_manager)