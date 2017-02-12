# coding=utf-8
import logging

from model.models import Comment

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
