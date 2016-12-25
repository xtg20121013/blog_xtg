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
