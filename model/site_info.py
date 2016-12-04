# coding=utf-8


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
