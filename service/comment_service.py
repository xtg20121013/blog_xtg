# coding=utf-8
import logging

from model.models import Comment
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)


class CommentService(object):

    @staticmethod
    def remove_by_article_id(db_session, article_id, commit=True):
        try:
            comments = db_session.query(Comment).filter(Comment.article_id == article_id).all()
            db_session.query(Comment).filter(Comment.article_id == article_id).delete()
            if commit:
                db_session.commit()
            return comments
        except Exception, e:
            logger.exception(e)
        return None

    @staticmethod
    def get_comments_count_subquery(db_session):
        stmt = db_session.query(Comment.article_id, func.count('*').label('comments_count')). \
            group_by(Comment.article_id).subquery()
        return stmt