# coding=utf-8
import os
import tornado.options
import tornado.web
import tornado.ioloop
from config import config

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
)

application = tornado.web.Application([
    (r"/", "controller.home.HomeHandler"),
], **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(config['server_port']);
    tornado.ioloop.IOLoop.current().start()