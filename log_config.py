# coding=utf-8
import logging
import logging.handlers
import tornado.log

FILE=dict(
    level="WARNING",
    log_path="logs/log", # 末尾自动添加 @端口号.txt_日期
    when="D", # 以什么单位分割文件
    interval=1, # 以上面的时间单位，隔几个单位分割文件
    backupCount=30, # 保留多少历史记录文件
    fmt="%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s",
)


def init(port, console_handler=False, file_handler=True, log_path=FILE['log_path'], base_level="INFO"):
    logger = logging.getLogger()
    logger.setLevel(base_level)
    # 配置控制台输出
    if console_handler:
        channel_console = logging.StreamHandler()
        channel_console.setFormatter(tornado.log.LogFormatter())
        logger.addHandler(channel_console)
    # 配置文件输出
    if file_handler:
        if not log_path:
            log_path = FILE['log_path']
        log_path = log_path+"@"+str(port)+".txt"
        formatter = logging.Formatter(FILE['fmt']);
        channel_file = logging.handlers.TimedRotatingFileHandler(
            filename=log_path,
            when=FILE['when'],
            interval=FILE['interval'],
            backupCount=FILE['backupCount'])
        channel_file.setFormatter(formatter)
        channel_file.setLevel(FILE['level'])
        logger.addHandler(channel_file)