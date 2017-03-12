# coding=utf-8
import logging
from apscheduler.schedulers.tornado import TornadoScheduler

logger = logging.getLogger(__name__)


class TimeTask(object):
    def __init__(self, sqlalchemy_engine):
        self.scheduler = TornadoScheduler()
        self.scheduler.add_jobstore("sqlalchemy", engine=sqlalchemy_engine)

    def add_cache_flush_task(self, func, *args, **kwargs):
        self.scheduler.add_job(func, 'cron', args=args, kwargs=kwargs,
                               id="cache_flush", replace_existing=True, hour=0, day='*')
        return self

    def start_tasks(self):
        self.scheduler.start()
