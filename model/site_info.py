# coding=utf-8
import json
import tornado.gen
from service import init_service
from config import site_cache_keys
from extends.utils import AlchemyEncoder, Dict


"""本页字段缓存策略
站点缓存，加快访问速度，尤其是首页显示的相关数据,该类字段做二级缓存，本地缓存-redis缓存
查询策略:先查本地缓存，未命中查询redis缓存，还未命中查询数据库，并将结果逐级更新
更新策略:数据写入数据库后，更新redis缓存，并通过发布对应字段的更新消息通知所有节点更新本地缓存
缓存校准:mater节点，设置定时任务，在访问较少的时间段校准redis缓存,并通知所有节点更新
"""


class SiteCollection(object):
    title = None                # string
    signature = None            # string
    navbar = None               # string
    menus = None                # json(list)
    article_types_not_under_menu = None # 不在menu下的article_types     #json(list)
    plugins = None              # JSON(list)
    blog_view_count = None      # int
    article_count = None        # int
    comment_count = None        # int
    article_sources = None      # JSON(list)

    @staticmethod
    @tornado.gen.coroutine
    def query_all(cache_manager, thread_do, db):
        yield SiteCollection.query_blog_info(cache_manager, thread_do, db)
        yield SiteCollection.query_menus(cache_manager, thread_do, db)
        yield SiteCollection.query_article_types_not_under_menu(cache_manager, thread_do, db)
        yield SiteCollection.query_plugins(cache_manager, thread_do, db)
        yield SiteCollection.query_blog_view_count(cache_manager, thread_do, db)
        yield SiteCollection.query_article_count(cache_manager, thread_do, db)
        yield SiteCollection.query_comment_count(cache_manager, thread_do, db)
        yield SiteCollection.query_article_sources(cache_manager, thread_do, db)

    @staticmethod
    @tornado.gen.coroutine
    def query_blog_info(cache_manager, thread_do, db):
        if SiteCollection.title is None or SiteCollection.signature is None \
                or SiteCollection.navbar is None:
            SiteCollection.title = yield cache_manager.call("GET", site_cache_keys['title'])
            SiteCollection.signature = yield cache_manager.call("GET", site_cache_keys['signature'])
            SiteCollection.navbar = yield cache_manager.call("GET", site_cache_keys['navbar'])
            if SiteCollection.title is None or SiteCollection.signature is None \
                    or SiteCollection.navbar is None:
                blog_info = yield thread_do(init_service.get_blog_info, db)
                SiteCollection.title = blog_info.title
                SiteCollection.signature = blog_info.signature
                SiteCollection.navbar = blog_info.navbar
                yield cache_manager.call("SET", site_cache_keys['title'], SiteCollection.title)
                yield cache_manager.call("SET", site_cache_keys['signature'], SiteCollection.signature)
                yield cache_manager.call("SET", site_cache_keys['navbar'], SiteCollection.navbar)

    @staticmethod
    @tornado.gen.coroutine
    def query_menus(cache_manager, thread_do, db):
        if SiteCollection.menus is None:
            menus_json = yield cache_manager.call("GET", site_cache_keys['menus'])
            if menus_json:
                menus = json.loads(menus_json, object_hook=Dict);
                SiteCollection.menus = menus
            if SiteCollection.menus is None:
                SiteCollection.menus = yield thread_do(init_service.get_menus, db)
                if SiteCollection.menus is not None:
                    menus_json = json.dumps(SiteCollection.menus, cls=AlchemyEncoder)
                    yield cache_manager.call("SET", site_cache_keys['menus'], menus_json)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_types_not_under_menu(cache_manager, thread_do, db):
        if SiteCollection.article_types_not_under_menu is None:
            ats_json = yield cache_manager.call("GET", site_cache_keys['article_types_not_under_menu'])
            if ats_json:
                ats = json.loads(ats_json, object_hook=Dict);
                SiteCollection.article_types_not_under_menu = ats
            if SiteCollection.article_types_not_under_menu is None:
                SiteCollection.article_types_not_under_menu = yield \
                    thread_do(init_service.get_article_types_not_under_menu, db)
                if SiteCollection.article_types_not_under_menu is not None:
                    ats_json = json.dumps(SiteCollection.article_types_not_under_menu, cls=AlchemyEncoder)
                    yield cache_manager.call("SET", site_cache_keys['article_types_not_under_menu'], ats_json)

    @staticmethod
    @tornado.gen.coroutine
    def query_plugins(cache_manager, thread_do, db):
        if SiteCollection.plugins is None:
            plugins_json = yield cache_manager.call("GET", site_cache_keys['plugins'])
            if plugins_json:
                plugins = json.loads(plugins_json, object_hook=Dict);
                SiteCollection.plugins = plugins
            if SiteCollection.plugins is None:
                SiteCollection.plugins = yield thread_do(init_service.get_plugins, db)
                if SiteCollection.plugins is not None:
                    plugins_json = json.dumps(SiteCollection.plugins, cls=AlchemyEncoder)
                    yield cache_manager.call("SET", site_cache_keys['plugins'], plugins_json)

    @staticmethod
    @tornado.gen.coroutine
    def query_blog_view_count(cache_manager, thread_do, db):
        if SiteCollection.blog_view_count is None:
            blog_view_count = yield cache_manager.call("GET", site_cache_keys['blog_view_count'])
            if blog_view_count is not None:
                SiteCollection.blog_view_count = int(blog_view_count)
            if SiteCollection.blog_view_count is None:
                SiteCollection.blog_view_count = yield thread_do(init_service.get_blog_view_count, db)
                if SiteCollection.blog_view_count is not None:
                    yield cache_manager.call("SET", site_cache_keys['blog_view_count'], SiteCollection.blog_view_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_count(cache_manager, thread_do, db):
        if SiteCollection.article_count is None:
            article_count = yield cache_manager.call("GET", site_cache_keys['article_count'])
            if article_count is not None:
                SiteCollection.article_count = int(article_count)
            if SiteCollection.article_count is None:
                SiteCollection.article_count = yield thread_do(init_service.get_article_count, db)
                if SiteCollection.article_count is not None:
                    yield cache_manager.call("SET", site_cache_keys['article_count'], SiteCollection.article_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_comment_count(cache_manager, thread_do, db):
        if SiteCollection.comment_count is None:
            comment_count = yield cache_manager.call("GET", site_cache_keys['comment_count'])
            if comment_count is not None:
                SiteCollection.comment_count = int(comment_count)
            if SiteCollection.comment_count is None:
                SiteCollection.comment_count = yield thread_do(init_service.get_comment_count, db)
                if SiteCollection.comment_count is not None:
                    yield cache_manager.call("SET", site_cache_keys['comment_count'], SiteCollection.comment_count)

    @staticmethod
    @tornado.gen.coroutine
    def query_article_sources(cache_manager, thread_do, db):
        if SiteCollection.article_sources is None:
            article_sources_json = yield cache_manager.call("GET", site_cache_keys['article_sources'])
            if article_sources_json:
                article_sources = json.loads(article_sources_json, object_hook=Dict);
                SiteCollection.article_sources = article_sources
            if SiteCollection.article_sources is None:
                SiteCollection.article_sources = yield thread_do(init_service.get_article_sources, db)
                if SiteCollection.article_sources is not None:
                    article_sources_json = json.dumps(SiteCollection.article_sources, cls=AlchemyEncoder)
                    yield cache_manager.call("SET", site_cache_keys['article_sources'], article_sources_json)
