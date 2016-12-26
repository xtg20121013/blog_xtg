# coding=utf-8
import logging
from sqlalchemy import func
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
                    menu.fetch_all_types()
        return menus
