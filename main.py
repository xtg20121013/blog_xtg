# coding=utf-8
import os

import concurrent.futures
import tornado.ioloop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options

import log_config
from config import config, redis_pub_sub_config, site_cache_config, redis_session_config
from controller.base import BaseHandler
from extends.cache_tornadis import CacheManager
from extends.session_tornadis import SessionManager
from extends.time_task import TimeTask
from service.init_service import flush_all_cache
from service.pubsub_service import PubSubService
from url_mapping import handlers

# tornado server相关参数
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
    default_handler_class=BaseHandler,
)


# sqlalchemy连接池配置以及生成链接池工厂实例
def db_poll_init():
    engine_config = config['database']['engine_url']
    engine = create_engine(engine_config, **config['database']["engine_setting"])
    config['database']['engine'] = engine
    db_poll = sessionmaker(bind=engine)
    return db_poll


def cache_manager_init():
    cache_manager = CacheManager(site_cache_config)
    return cache_manager


# 继承tornado.web.Application类，可以在构造函数里做站点初始化（初始数据库连接池，初始站点配置，初始异步线程池，加载站点缓存等）
class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session'])
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num'])
        self.db_pool = db_poll_init()
        self.cache_manager = cache_manager_init()
        self.pubsub_manager = None


#  从命令行读取配置，如果这些参数不传，默认使用config.py的配置项
def parse_command_line():
    options.define("port", help="run server on a specific port", type=int)
    options.define("log_console", help="print log to console", type=bool)
    options.define("log_file", help="print log to file", type=bool)
    options.define("log_file_path", help="path of log_file", type=str)
    options.define("log_level", help="level of logging", type=str)
    # 集群中最好有且仅有一个实例为master，一般用于执行全局的定时任务
    options.define("master", help="is master node? (true:master / false:slave)", type=bool)
    # sqlalchemy engine_url, 例如pgsql 'postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog'
    options.define("engine_url", help="engine_url for sqlalchemy", type=str)
    # redis相关配置, 覆盖所有用到redis位置的配置
    options.define("redis_host", help="redis host e.g 127.0.0.1", type=str)
    options.define("redis_port", help="redis port e.g 6379", type=int)
    options.define("redis_password", help="redis password set this option if has pwd ", type=str)
    options.define("redis_db", help="redis db e.g 0", type=int)

    # 读取 项目启动时，命令行上添加的参数项
    options.parse_command_line()
    # 覆盖默认的config配置
    if options.port is not None:
        config['port'] = options.port
    if options.log_console is not None:
        config['log_console'] = options.log_console
    if options.log_file is not None:
        config['log_file'] = options.log_file
    if options.log_file_path is not None:
        config['log_file_path'] = options.log_file_path
    if options.log_level is not None:
        config['log_level'] = options.log_level
    if options.master is not None:
        config['master'] = options.master
    if options.engine_url is not None:
        config['database']['engine_url'] = options.engine_url
    if options.redis_host is not None:
        redis_session_config['host'] = options.redis_host
        site_cache_config['host'] = options.redis_host
        redis_pub_sub_config['host'] = options.redis_host
    if options.redis_port is not None:
        redis_session_config['port'] = options.redis_port
        site_cache_config['port'] = options.redis_port
        redis_pub_sub_config['port'] = options.redis_port
    if options.redis_password is not None:
        redis_session_config['password'] = options.redis_password
        site_cache_config['password'] = options.redis_password
        redis_pub_sub_config['password'] = options.redis_password
    if options.redis_db is not None:
        redis_session_config['db_no'] = options.redis_db
        site_cache_config['db_no'] = options.redis_db


if __name__ == '__main__':
    # 加载命令行配置
    parse_command_line()
    # 加载日志管理
    options.logging = None  # 不用tornado自带的logging配置
    log_config.init(config['port'], config['log_console'],
                    config['log_file'], config['log_file_path'], config['log_level'])
    application = Application()
    application.listen(config['port'])
    # 全局注册application
    config['application'] = application
    loop = tornado.ioloop.IOLoop.current()
    # 加载redis消息监听客户端
    pubsub_manager = PubSubService(redis_pub_sub_config, application, loop)
    pubsub_manager.long_listen()
    application.pubsub_manager = pubsub_manager
    # 为master节点注册定时任务
    if config['master']:
        TimeTask(config['database']['engine']).add_cache_flush_task(flush_all_cache).start_tasks()
    loop.start()
