# coding=utf-8


# 基本站点配置,项目初始化时从数据库中导入
class SiteCollection:
    title = None
    signature = None
    navbar = None
    menus = None
    article_types_not_under_menu = None # 不在menu下的article_types
    plugins = None
    blog_view_count = 0
    article_count = 0
    comment_count = 0
    article_sources = None

    def __init__(self):
        pass