# coding=utf-8

cookie_keys = dict(
    session_key_name="TR_SESSION_ID",
    uv_key_name="uv_tag",
)

# session相关配置（redis实现）
redis_session_config = dict(
    db_no=0,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
    session_key_name=cookie_keys['session_key_name'],
    session_expires_days=7,
)

# 站点缓存(redis)
site_cache_config = dict(
    db_no=1,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
)

# 基于redis的消息订阅（发布接收缓存更新消息）
redis_pub_sub_channels = dict(
    cache_message_channel="site_cache_message_channel",
)

# 消息订阅(基于redis)配置
redis_pub_sub_config = dict(
    host="127.0.0.1",
    port=6379,
    password=None,
    autoconnect=True,
    channels=[redis_pub_sub_channels['cache_message_channel'],],
)

# 数据库配置
database_config = dict(
    engine=None,
    # engine_url='postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog',
    # 如果是使用mysql+mysqldb，在确认所有的库表列都是uft8编码后，依然有字符编码报错，
    # 可以尝试在该url末尾加上queryString charset=utf8
    engine_url='mysql+mysqldb://root:86DUlinxiang@localhost:3306/blog_xtg?charset=utf8',
    engine_setting=dict(
        echo=False,  # print sql
        echo_pool=False,
        # 设置7*60*60秒后回收连接池，默认-1，从不重置
        # 该参数会在每个session调用执行sql前校验当前时间与上一次连接时间间隔是否超过pool_recycle，如果超过就会重置。
        # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
        # 如果mysql重启或断开过连接，那么依然会在第一次时报"MySQL server has gone away"，
        # 假如需要非常严格的mysql断线重连策略，可以设置心跳。
        # 心跳设置参考https://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away
        pool_recycle=25200,
        pool_size=20,
        max_overflow=20,
    ),
)

session_keys = dict(
    login_user="login_user",
    messages="messages",
    article_draft="article_draft",
)

# 关联model.site_info中的字段
site_cache_keys = dict(
    title="title",
    signature="signature",
    navbar="navbar",
    menus="menus",
    article_types_not_under_menu="article_types_not_under_menu",
    plugins="plugins",
    pv="pv",
    uv="uv",
    article_count="article_count",
    comment_count="comment_count",
    article_sources="article_sources",
    source_articles_count="source_{}_articles_count",
)

# 站点相关配置以及tornado的相关参数
config = dict(
    debug=False,
    log_level="WARNING",
    log_console=False,
    log_file=True,
    log_file_path="logs/log",  # 末尾自动添加 @端口号.txt_日期
    compress_response=True,
    xsrf_cookies=True,
    cookie_secret="kjsdhfweiofjhewnfiwehfneiwuhniu",
    login_url="/auth/login",
    port=8888,
    max_threads_num=500,
    database=database_config,
    redis_session=redis_session_config,
    session_keys=session_keys,
    master=True,  # 是否为主从节点中的master节点, 整个集群有且仅有一个,(要提高可用性的话可以用zookeeper来选主,该项目就暂时不做了)
    navbar_styles={"inverse": "魅力黑", "default": "优雅白"},  # 导航栏样式
    default_avatar_url="identicon",
    application=None,  # 项目启动后会在这里注册整个server，以便在需要的地方调用，勿修改
)

# 评论功能的邮件发送
email = dict(
    email_host="smtp.qq.com",
    stmp_port=465,
    email_user="admin@dearx.me",  # 邮箱账户，特别注意邮箱需要打开smtp功能，比如qq邮箱，请自行搜索如何打开smtp功能
    email_pw="hwpgddtpqjqtcbee" # 邮箱的密码，特别注意邮箱需要打开smtp功能
)