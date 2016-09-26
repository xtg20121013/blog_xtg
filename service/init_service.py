# coding=utf-8
from model.models import BlogInfo, Menu, ArticleType, Plugin, BlogView, Article, Comment, Source
from model.site_info import SiteCollection
from sqlalchemy.orm import joinedload


def site_init(db_session):
    blog_info_init(db_session)
    menu_init(db_session)
    plugin_init(db_session)
    blog_view_init(db_session)
    article_count_init(db_session)
    comment_count_init(db_session)
    article_sources_init(db_session)


def blog_info_init(db_session):
    blog = db_session.query(BlogInfo).first()
    if blog:
        SiteCollection.title = blog.title
        SiteCollection.signature = blog.signature
        SiteCollection.navbar = blog.navbar


def menu_init(db_session):
    menus = db_session.query(Menu).order_by(Menu.order.asc()).all()
    if menus:
        SiteCollection.menus = menus
    else:
        SiteCollection.menus = []
    article_types_not_under_menu = db_session.query(ArticleType).options(joinedload(ArticleType.setting))\
        .filter(ArticleType.menu_id.is_(None)).all()
    if article_types_not_under_menu:
        SiteCollection.article_types_not_under_menu = article_types_not_under_menu


def plugin_init(db_session):
    plugins = db_session.query(Plugin).order_by(Plugin.order.asc()).all()
    if plugins:
        SiteCollection.plugins = plugins


def blog_view_init(db_session):
    SiteCollection.blog_view_count = db_session.query(BlogView).first().num_of_view


def article_count_init(db_session):
    SiteCollection.article_count = db_session.query(Article).count()


def comment_count_init(db_session):
    SiteCollection.comment_count = db_session.query(Comment).count()


def article_sources_init(db_session):
    article_sources = db_session.query(Source).all()
    if article_sources:
        for source in article_sources:
            source.fetch_articles_count()
        SiteCollection.article_sources = article_sources