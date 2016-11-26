# coding=utf-8
from model.models import BlogInfo, Menu, ArticleType, Plugin, BlogView, Article, Comment, Source
from sqlalchemy.orm import joinedload

"""
从数据库获取站点(model.site_info)缓存
"""


def get_blog_info(db_session):
    blog = db_session.query(BlogInfo).first()
    return blog


def get_menus(db_session):
    menus = db_session.query(Menu).order_by(Menu.order.asc()).all()
    if not menus:
        menus = []
    return menus


def get_article_types_not_under_menu(db_session):
    article_types_not_under_menu = db_session.query(ArticleType).options(joinedload(ArticleType.setting))\
        .filter(ArticleType.menu_id.is_(None)).all()
    return article_types_not_under_menu


def get_plugins(db_session):
    plugins = db_session.query(Plugin).order_by(Plugin.order.asc()).all()
    return plugins


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
