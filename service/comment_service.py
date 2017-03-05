# coding=utf-8
import logging

from model.models import Comment
from sqlalchemy.sql import func
from . import BaseService

logger = logging.getLogger(__name__)


class CommentService(object):
    @staticmethod
    def get_comment(db_session, comment_id):
        return db_session.query(Comment).get(comment_id)

    @staticmethod
    def get_max_floor(db_session, article_id):
        max_floor = db_session.query(func.max(Comment.floor)).filter(Comment.article_id == article_id).scalar()
        return max_floor if max_floor else 0;

    @staticmethod
    def add_comment(db_session, article_id, comment):
        max_floor = CommentService.get_max_floor(db_session, article_id)
        floor = max_floor + 1
        comment_to_add = Comment(content=comment['content'], author_name=comment['author_name'],
                                 author_email=comment['author_email'], article_id=article_id,
                                 comment_type=comment['comment_type'], rank=comment['rank'], floor=floor,
                                 reply_to_id=comment['reply_to_id'], reply_to_floor=comment['reply_to_floor'])
        db_session.add(comment_to_add)
        db_session.commit()
        return comment_to_add

    @staticmethod
    def update_comment_disabled(db_session, article_id, comment_id, disabled):
        updated = db_session.query(Comment).filter(Comment.article_id == article_id, Comment.id == comment_id).\
            update({Comment.disabled: disabled})
        db_session.commit()
        return updated

    @staticmethod
    def page_comments(db_session, pager, article_id):
        query = db_session.query(Comment).filter(Comment.article_id == article_id)
        query = query.order_by(Comment.create_time.asc())
        pager = BaseService.query_pager(query, pager)
        return pager

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