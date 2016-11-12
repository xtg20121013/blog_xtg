# coding=utf-8
import os
import log_config
from config import config
from tornado.options import options
import tornado.ioloop
import concurrent.futures
import controller.home
from tornado.web import url
from extends.session_tornadis import SessionManager
from service.init_service import site_init
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# tornado server相关参数
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
)


# url映射
handlers = [
    url(r"/", controller.home.HomeHandler, name="index"),
    url(r"/auth/login", controller.home.LoginHandler, name="login"),
    url(r"/([0-9]+)", controller.home.HomeHandler, name="articleTypes"),
    url(r"/auth/logout", controller.home.LogoutHandler, name="logout"),
    url(r"/([0-9]+)", controller.home.HomeHandler, name="articleSources"),
    url(r"/", controller.home.HomeHandler, name="admin.submitArticles"),
    url(r"/", controller.home.HomeHandler, name="admin.account"),
]


# sqlalchemy连接池配置以及生成链接池工厂实例
def db_poll_init():
    engine_config = config['database']['engine_url']
    engine = create_engine(engine_config, **config['database']["engine_setting"])
    db_poll = sessionmaker(bind=engine)
    return db_poll;


# 继承tornado.web.Application类，可以在构造函数里做站点初始化（初始数据库连接池，初始站点配置，初始异步线程池，加载站点缓存等）
class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session'])
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num'])
        self.db_pool = db_poll_init()
        site_init(self.db_pool())

if __name__ == '__main__':
    options.define("port", default=config['default_server_port'], help="run server on a specific port", type=int)
    options.define("console_log", default=False, help="print log to console", type=bool)
    options.define("file_log", default=True, help="print log to file", type=bool)
    options.define("file_log_path", default=log_config.FILE['log_path'], help="path of log_file", type=str)
    options.logging = None
    # 读取 项目启动时，命令行上添加的参数项
    options.parse_command_line()
    # 加载日志管理
    log_config.init(options.port, options.console_log, options.file_log, options.file_log_path)
    Application().listen(options.port);
    tornado.ioloop.IOLoop.current().start()