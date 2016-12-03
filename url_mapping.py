# coding=utf-8
import controller.home
import controller.admin
import controller.admin_custom
from tornado.web import url


# url映射
handlers = [
    url(r"/", controller.home.HomeHandler, name="index"),
    url(r"/auth/login", controller.home.LoginHandler, name="login"),
    url(r"/auth/login/(\d+)", controller.home.LoginHandler),
    url(r"/([0-9]+)", controller.home.HomeHandler, name="articleTypes"),
    url(r"/auth/logout", controller.home.LogoutHandler, name="logout"),
    url(r"/([0-9]+)", controller.home.HomeHandler, name="articleSources"),
    # admin
    url(r"/admin/account", controller.admin.AdminAccountHandler, name="admin.account"),
    url(r"/admin/help", controller.admin.AdminHelpHandler, name="admin.help"),
    url(r"/admin/account/(.+)", controller.admin.AdminAccountHandler, name="admin.account.update"),
    # admin.custom
    url(r"/admin/custom/blog-info", controller.admin_custom.AdminCustomBlogInfoHandler, name="admin.custom.blog_info"),
    url(r"/", controller.home.HomeHandler, name="admin.custom.blog_plugin"),
    url(r"/", controller.home.HomeHandler, name="admin.custom.add_plugin"),

    url(r"/", controller.home.HomeHandler, name="admin.submitArticles"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_articles"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_articleTypes"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_comments"),


]