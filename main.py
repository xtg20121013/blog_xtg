# coding=utf-8
import os
import tornado.options
import tornado.web
import tornado.ioloop
from config import config
from extends.session_tornadis import SessionManager

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
    (r"/", "controller.home.HomeHandler"),
]


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session'])


if __name__ == '__main__':
    # tornado.options.parse_command_line()
    Application().listen(config['server_port']);
    tornado.ioloop.IOLoop.current().start()