# coding=utf-8
import controller.home
import controller.admin
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
    url(r"/", controller.home.HomeHandler, name="admin.submitArticles"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_articles"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_articleTypes"),
    url(r"/", controller.home.HomeHandler, name="admin.manage_comments"),
    url(r"/", controller.home.HomeHandler, name="admin.custom_blog_info"),
    url(r"/", controller.home.HomeHandler, name="admin.custom_blog_plugin"),
    url(r"/", controller.home.HomeHandler, name="admin.add_plugin"),
    url(r"/admin/help", controller.admin.AdminHelpHandler, name="admin.help"),
    url(r"/admin/account/(.+)", controller.admin.AdminAccountHandler, name="admin.account.update"),
]