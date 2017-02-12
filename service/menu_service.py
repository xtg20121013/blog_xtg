# coding=utf-8
import logging

from sqlalchemy import func

from article_type_service import ArticleTypeService
from model.models import Menu
from model.search_params.menu_params import MenuSearchParams
from . import BaseService

logger = logging.getLogger(__name__)


class MenuService(object):
    @staticmethod
    def page_menus(db_session, pager, search_params):
        query = db_session.query(Menu)
        if search_params:
            if search_params.order_mode == MenuSearchParams.ORDER_MODE_ORDER_ASC:
                query = query.order_by(Menu.order.asc())
        pager = BaseService.query_pager(query, pager)
        if pager.result:
            for menu in pager.result:
                menu.fetch_all_types()
        return pager

    @staticmethod
    def add_menu(db_session, menu):
        try:
            menu_to_save = Menu(**menu)
            menu_to_save.order = MenuService.get_max_order(db_session) + 1
            db_session.add(menu_to_save)
            db_session.commit()
            return menu_to_save
        except Exception, e:
            logger.exception(e)
        return None

    @staticmethod
    def get_max_order(db_session):
        max_order = db_session.query(func.max(Menu.order)).scalar()
        if max_order is None:
            max_order = 0
        return max_order

    @staticmethod
    def list_menus(db_session, show_types=False):
        menus = db_session.query(Menu).order_by(Menu.order.asc()).all()
        if not menus:
            menus = []
        else:
            if show_types:
                for menu in menus:
                    menu.fetch_all_types(only_show_not_hide=True)
        return menus

    @staticmethod
    def sort_up(db_session, menu_id):
        menu = db_session.query(Menu).get(menu_id)
        if menu:
            menu_up = db_session.query(Menu). \
                filter(Menu.order < menu.order).order_by(Menu.order.desc()).first()
            if menu_up:
                order_tmp = menu.order
                menu.order = menu_up.order
                menu_up.order = order_tmp
                db_session.commit()
                return True
        return False

    @staticmethod
    def sort_down(db_session, menu_id):
        menu = db_session.query(Menu).get(menu_id)
        if menu:
            menu_up = db_session.query(Menu). \
                filter(Menu.order > menu.order).order_by(Menu.order.asc()).first()
            if menu_up:
                order_tmp = menu.order
                menu.order = menu_up.order
                menu_up.order = order_tmp
                db_session.commit()
                return True
        return False

    @staticmethod
    def update(db_session, menu_id, menu_to_update):
        count = 0
        if menu_to_update:
            if "id" in menu_to_update:
                menu_to_update.remove("id")
            count = db_session.query(Menu).filter(Menu.id == menu_id).update(menu_to_update)
            if count:
                db_session.commit()
        return count

    @staticmethod
    def delete(db_session, menu_id):
        ArticleTypeService.set_article_type_menu_id_none(db_session, menu_id, auto_commit=False)
        count = db_session.query(Menu).filter(Menu.id == menu_id).delete()
        if count:
            db_session.commit()
        return count
