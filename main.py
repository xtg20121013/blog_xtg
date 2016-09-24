# coding=utf-8
import os
from config import config  # 必须放在tornado导入前，接管全局logging
import tornado.web
import tornado.ioloop
import concurrent.futures
import controller.home
from tornado.web import url
from extends.session_tornadis import SessionManager
from service.init_service import site_init
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
)

handlers = [
    url(r"/", controller.home.HomeHandler, name="index"),
    url(r"/", controller.home.HomeHandler, name="articleTypes"),
]


def db_poll_init():
    engine_config = config['database']['engine_config']
    engine = create_engine(engine_config, echo=config['database']['sql_echo'])
    db_poll = sessionmaker(bind=engine)
    return db_poll;


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session'])
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num'])
        self.db_pool = db_poll_init()
        site_init(self.db_pool())

if __name__ == '__main__':
    Application().listen(config['server_port']);
    tornado.ioloop.IOLoop.current().start()