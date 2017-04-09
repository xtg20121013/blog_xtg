# coding=utf-8
import logging
import datetime
from model.models import BlogView

logger = logging.getLogger(__name__)


class BlogViewService(object):
    @staticmethod
    def get_blog_view(db_session, date=None):
        if not date:
            date = datetime.date.today()
        blog_view = db_session.query(BlogView).get(date)
        return blog_view

    @staticmethod
    def add_blog_view(db_session, add_pv, add_uv, date=None):
        if not date:
            date = datetime.date.today()
        blog_view = BlogViewService.get_blog_view(db_session, date)
        if blog_view:
            blog_view.pv = BlogView.pv + add_pv
            blog_view.uv = BlogView.uv + add_uv
        else:
            blog_view = BlogView(date=date, pv=add_pv, uv=add_uv)
            db_session.add(blog_view)
        db_session.commit()
        return blog_view
