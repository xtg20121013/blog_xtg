# coding=utf-8
import logging
from sqlalchemy.orm import contains_eager, joinedload
from model.models import ArticleType, ArticleTypeSetting
from model.search_params.article_type_params import ArticleTypeSearchParams
from . import BaseService

logger = logging.getLogger(__name__)


class ArticleTypeService(object):
    @staticmethod
    def page_article_types(db_session, pager, search_params):
        query = db_session.query(ArticleType)
        if search_params:
            if search_params.order_mode == ArticleTypeSearchParams.ORDER_MODE_ID_DESC:
                query = query.order_by(ArticleType.id.desc())
            if search_params.show_setting:
                query = query.options(joinedload(ArticleType.setting))
        pager = BaseService.query_pager(query, pager)
        if pager.result:
            if search_params.show_articles_count:
                for article_type in pager.result:
                    article_type.fetch_articles_count()
        return pager

    @staticmethod
    def list_article_types_not_under_menu(db_session):
        article_types_not_under_menu = db_session.query(ArticleType).join(ArticleType.setting).\
            filter(ArticleType.menu_id.is_(None), ArticleTypeSetting.hide.isnot(True)).\
            options(contains_eager(ArticleType.setting)).all()
        return article_types_not_under_menu

    @staticmethod
    def add_article_type(db_session, article_type):
        try:
            article_type_to_add = ArticleType(name=article_type["name"], introduction=article_type["introduction"],
                                              menu_id=article_type["menu_id"],
                                              setting=ArticleTypeSetting(name=article_type["name"],
                                                                         hide=article_type["setting_hide"],),)
            db_session.add(article_type_to_add)
            db_session.commit()
            return article_type_to_add
        except Exception, e:
            logger.exception(e)
        return None

    @staticmethod
    def update_article_type(db_session, article_type_id, article_type):
        try:
            article_type_to_update=db_session.query(ArticleType).get(article_type_id)
            if article_type_to_update and not article_type_to_update.is_protected:
                article_type_to_update.name=article_type['name']
                article_type_to_update.introduction = article_type['introduction']
                article_type_to_update.menu_id = article_type['menu_id']
                if not article_type_to_update.setting:
                    article_type_to_update.setting = ArticleTypeSetting(name=article_type["name"],
                                                                        hide=article_type["setting_hide"],)
                else:
                    article_type_to_update.setting.hide = article_type['setting_hide']
                db_session.commit()
                return True
        except Exception, e:
            logger.exception(e)
        return False

    @staticmethod
    def delete(db_session, article_type_id):
        article_type_to_delete = db_session.query(ArticleType).get(article_type_id)
        if article_type_to_delete and not article_type_to_delete.is_protected:
            # 未将文章分类移除到未分类
            db_session.delete(article_type_to_delete.setting)
            db_session.delete(article_type_to_delete)
            db_session.commit()
            return 1
        return 0

    @staticmethod
    def set_article_type_menu_id_none(db_session, menu_id, auto_commit=True):
        db_session.query(ArticleType).filter(ArticleType.menu_id == menu_id).update({"menu_id": None})
        if auto_commit:
            db_session.commit()

    @staticmethod
    def list_simple(db_session):
        article_types = db_session.query(ArticleType.id, ArticleType.name).all()
        return article_types
