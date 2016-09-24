# coding=utf-8
from model.models import BlogInfo, Menu, ArticleType
from model.site_info import SiteCollection


def site_init(db_session):
    blog_info_init(db_session)
    menu_init(db_session)


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
    article_types_not_under_menu = db_session.query(ArticleType).filter(ArticleType.menu_id.is_(None)).all()
    if article_types_not_under_menu:
        SiteCollection.article_types_not_under_menu = article_types_not_under_menu
