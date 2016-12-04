# coding=utf-8
from base import BaseHandler
from tornado.gen import coroutine
from tornado.web import authenticated
from config import config
from service.custom_service import BlogInfoService
from service.init_service import SiteCacheService


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
            yield SiteCacheService.update_blog_info(self.cache_manager, self.pubsub_manager, blog_info)
            self.add_message('success', u'修改博客信息成功!')
        else:
            self.add_message('danger', u'修改失败！')
        self.redirect(self.reverse_url("admin.custom.blog_info"))