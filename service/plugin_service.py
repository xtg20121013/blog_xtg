# coding=utf-8
import logging
from sqlalchemy import func
from model.models import Plugin
from model.search_params.plugin_params import PluginSearchParams
from . import BaseService

logger = logging.getLogger(__name__)


class PluginService(object):

    @staticmethod
    def list_plugins(db_session):
        plugins = db_session.query(Plugin).order_by(Plugin.order.asc()).all()
        return plugins

    @staticmethod
    def page_plugins(db_session, pager, search_params):
        query = db_session.query(Plugin)
        if not search_params:
            if search_params.order_mode == PluginSearchParams.ORDER_MODE_ORDER_ASC:
                query = query.order_by(Plugin.order.asc())
        pager = BaseService.query_pager(query, pager)
        return pager

    @staticmethod
    def save(db_session, plugin):
        try:
            plugin_to_save = Plugin(**plugin)
            plugin_to_save.order = PluginService.get_max_order(db_session) + 1
            db_session.add(plugin_to_save)
            db_session.commit()
            return plugin_to_save
        except Exception, e:
            logger.exception(e)
        return None

    @staticmethod
    def get_max_order(db_session):
        max_order = db_session.query(func.max(Plugin.order)).scalar()
        if max_order is None:
            max_order = 0
        return max_order
