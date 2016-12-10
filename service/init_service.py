# coding=utf-8
import json
import tornado.gen
from config import site_cache_keys
from extends.utils import AlchemyEncoder, Dict
from model.models import Menu, ArticleType, Plugin, BlogView, Article, Comment, Source
from sqlalchemy.orm import joinedload
from custom_service import BlogInfoService
from plugin_service import PluginService
from model.site_info import SiteCollection


"""
初始化相关，包括缓存管理
"""


class SiteCacheService(object):
    """SiteCache缓存策略
    站点缓存，加快访问速度，尤其是首页显示的相关数据,该类字段做二级缓存，本地缓存-redis缓存
    查询策略:先查本地缓存，未命中查询redis缓存，还未命中查询数据库，并将结果逐级更新
    更新策略:数据写入数据库后，更新redis缓存，并通过发布对应字段的更新消息通知所有节点更新本地缓存
    缓存校准:mater节点，设置定时任务，在访问较少的时间段校准redis缓存,并通知所有节点更新
    """
    PUB_SUB_MSGS = dict(
        blog_info_updated="blog_info_updated",  # blog_info更新消息
        plugins_updated="plugins_updated",  # plugins更新消息
    )

    @staticmethod
    @tornado.gen.coroutine
    def query_all(cache_manager, thread_do, db):
        yield SiteCacheService.query_blog_info(cache_manager, thread_do, db)
        yield SiteCacheService.query_menus(cache_manager, thread_do, db)
        yield SiteCacheService.query_article_types_not_under_menu(cache_manager, thread_do, db)
        yield SiteCacheService.query_plugins(cache_manager, thread_do, db)
        yield SiteCacheService.query_blog_view_count(cache_manager, thread_do, db)
        yield SiteCacheService.query_article_count(cache_manager, thread_do, db)
        yield SiteCacheService.query_comment_count(cache_manager, thread_do, db)
        yield SiteCacheService.query_article_sources(cache_manager, thread_do, db)

    @staticmethod
    @tornado.gen.coroutine
    def query_blog_info(cache_manager, thread_do, db):
        SiteCollection.title = yield cache_manager.call("GET", site_cache_keys['title'])
        SiteCollection.signature = yield cache_manager.call("GET", site_cache_keys['signature'])
        SiteCollection.navbar = yield cache_manager.call("GET", site_cache_keys['navbar'])
        if SiteCollection.title is None or SiteCollection.signature is None or SiteCollection.navbar is None:
            blog_info = yield thread_do(BlogInfoService.get_blog_info, db)
            yield SiteCacheService.update_blog_info(cache_manager, blog_info)

    @staticmethod
    @tornado.gen.coroutine
    def query_menus(cache_manager, thread_do, db):
        menus_json = yield cache_manager.call("GET", site_cache_keys['menus'])
        if menus_json:
            menus = json.loads(menus_json, object_hook=Dict);
            SiteCollection.menus = menus
        if SiteCollection.menus is None:
            SiteCollection.menus = yield thread_do(get_menus, db)
            if SiteCollection.menus is not None:
                menus_json = json.dumps(SiteCollection.menus, cls=AlchemyEncoder)
                yield cache_manager.call("SET", site_cache_keys['menus'], menus_json)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_types_not_under_menu(cache_manager, thread_do, db):
        ats_json = yield cache_manager.call("GET", site_cache_keys['article_types_not_under_menu'])
        if ats_json:
            ats = json.loads(ats_json, object_hook=Dict);
            SiteCollection.article_types_not_under_menu = ats
        if SiteCollection.article_types_not_under_menu is None:
            SiteCollection.article_types_not_under_menu = yield thread_do(get_article_types_not_under_menu, db)
            if SiteCollection.article_types_not_under_menu is not None:
                ats_json = json.dumps(SiteCollection.article_types_not_under_menu, cls=AlchemyEncoder)
                yield cache_manager.call("SET", site_cache_keys['article_types_not_under_menu'], ats_json)

    @staticmethod
    @tornado.gen.coroutine
    def query_plugins(cache_manager, thread_do, db):
        plugins_json = yield cache_manager.call("GET", site_cache_keys['plugins'])
        if plugins_json:
            plugins = json.loads(plugins_json, object_hook=Dict);
            SiteCollection.plugins = plugins
        if SiteCollection.plugins is None:
            plugins = yield thread_do(PluginService.list_plugins, db)
            yield SiteCacheService.update_plugins(cache_manager, plugins)

    @staticmethod
    @tornado.gen.coroutine
    def query_blog_view_count(cache_manager, thread_do, db):
        blog_view_count = yield cache_manager.call("GET", site_cache_keys['blog_view_count'])
        if blog_view_count is not None:
            SiteCollection.blog_view_count = int(blog_view_count)
        if SiteCollection.blog_view_count is None:
            SiteCollection.blog_view_count = yield thread_do(get_blog_view_count, db)
            if SiteCollection.blog_view_count is not None:
                yield cache_manager.call("SET", site_cache_keys['blog_view_count'], SiteCollection.blog_view_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_count(cache_manager, thread_do, db):
        article_count = yield cache_manager.call("GET", site_cache_keys['article_count'])
        if article_count is not None:
            SiteCollection.article_count = int(article_count)
        if SiteCollection.article_count is None:
            SiteCollection.article_count = yield thread_do(get_article_count, db)
            if SiteCollection.article_count is not None:
                yield cache_manager.call("SET", site_cache_keys['article_count'], SiteCollection.article_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_comment_count(cache_manager, thread_do, db):
        comment_count = yield cache_manager.call("GET", site_cache_keys['comment_count'])
        if comment_count is not None:
            SiteCollection.comment_count = int(comment_count)
        if SiteCollection.comment_count is None:
            SiteCollection.comment_count = yield thread_do(get_comment_count, db)
            if SiteCollection.comment_count is not None:
                yield cache_manager.call("SET", site_cache_keys['comment_count'], SiteCollection.comment_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_sources(cache_manager, thread_do, db):
        article_sources_json = yield cache_manager.call("GET", site_cache_keys['article_sources'])
        if article_sources_json:
            article_sources = json.loads(article_sources_json, object_hook=Dict);
            SiteCollection.article_sources = article_sources
        if SiteCollection.article_sources is None:
            SiteCollection.article_sources = yield thread_do(get_article_sources, db)
            if SiteCollection.article_sources is not None:
                article_sources_json = json.dumps(SiteCollection.article_sources, cls=AlchemyEncoder)
                yield cache_manager.call("SET", site_cache_keys['article_sources'], article_sources_json)

# 下面是缓存更新

    @staticmethod
    @tornado.gen.coroutine
    def update_by_sub_msg(msg, cache_manager, thread_do, db):
        if not msg:
            pass
        elif msg == SiteCacheService.PUB_SUB_MSGS['blog_info_updated']:
            yield SiteCacheService.query_blog_info(cache_manager, thread_do, db)
        elif msg == SiteCacheService.PUB_SUB_MSGS['plugins_updated']:
            yield SiteCacheService.query_plugins(cache_manager, thread_do, db)

    @staticmethod
    @tornado.gen.coroutine
    def update_blog_info(cache_manager, blog_info, is_pub_all=False, pubsub_manager=None):
        SiteCollection.title = blog_info.title
        SiteCollection.signature = blog_info.signature
        SiteCollection.navbar = blog_info.navbar
        yield cache_manager.call("SET", site_cache_keys['title'], blog_info.title)
        yield cache_manager.call("SET", site_cache_keys['signature'], blog_info.signature)
        yield cache_manager.call("SET", site_cache_keys['navbar'], blog_info.navbar)
        if is_pub_all:
            yield pubsub_manager.pub_call(SiteCacheService.PUB_SUB_MSGS['blog_info_updated'])

    @staticmethod
    @tornado.gen.coroutine
    def update_plugins(cache_manager, plugins, is_pub_all=False, pubsub_manager=None):
        if plugins is not None:
            SiteCollection.plugins = plugins
            plugins_json = json.dumps(plugins, cls=AlchemyEncoder)
            yield cache_manager.call("SET", site_cache_keys['plugins'], plugins_json)
            if is_pub_all:
                yield pubsub_manager.pub_call(SiteCacheService.PUB_SUB_MSGS['plugins_updated'])


def get_menus(db_session):
    menus = db_session.query(Menu).order_by(Menu.order.asc()).all()
    if not menus:
        menus = []
    return menus


def get_article_types_not_under_menu(db_session):
    article_types_not_under_menu = db_session.query(ArticleType).options(joinedload(ArticleType.setting))\
        .filter(ArticleType.menu_id.is_(None)).all()
    return article_types_not_under_menu


def get_blog_view_count(db_session):
    blog_view_count = db_session.query(BlogView).first().num_of_view
    return blog_view_count


def get_article_count(db_session):
    article_count = db_session.query(Article).count()
    return article_count


def get_comment_count(db_session):
    comment_count = db_session.query(Comment).count()
    return comment_count


def get_article_sources(db_session):
    article_sources = db_session.query(Source).all()
    if article_sources:
        for source in article_sources:
            source.fetch_articles_count()
    return article_sources
