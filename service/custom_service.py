# coding=utf-8
from model.models import BlogInfo

"""
博客定制相关服务
"""


class BlogInfoService(object):

    @staticmethod
    def get_blog_info(db_session):
        blog = db_session.query(BlogInfo).first()
        return blog

    @staticmethod
    def update_blog_info(db_session, blog_info):
        blog_info_old = BlogInfoService.get_blog_info(db_session)
        if blog_info_old is not None:
            if "title" in blog_info and blog_info['title'] is not None:
                blog_info_old.title = blog_info['title']
            if "signature" in blog_info and blog_info['signature'] is not None:
                blog_info_old.signature = blog_info['signature']
            if "navbar" in blog_info and blog_info['navbar'] is not None:
                blog_info_old.navbar = blog_info['navbar']
            db_session.commit()
        return blog_info_old
