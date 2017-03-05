# coding=utf-8

# session相关配置（redis实现）
redis_session_config = dict(
    db_no=0,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
    session_key_name="TR_SESSION_ID",
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
    engine_url='postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog',
    engine_setting=dict(
        echo=True,
        echo_pool=False,
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
    blog_view_count="blog_view_count",
    article_count="article_count",
    comment_count="comment_count",
    article_sources="article_sources",
    source_articles_count="source_{}_articles_count",
)

# 站点相关配置以及tornado的相关参数
config = dict(
    debug=True,
    compress_response=True,
    xsrf_cookies=True,
    cookie_secret="kjsdhfweiofjhewnfiwehfneiwuhniu",
    login_url="/auth/login",
    default_server_port=8888,
    max_threads_num=500,
    database=database_config,
    redis_session=redis_session_config,
    session_keys=session_keys,
    default_master=False,  # 是否为主从节点中的master节点,
    navbar_styles={"inverse":"魅力黑", "default":"优雅白"},  # 导航栏样式
    default_avatar_url=None,  # "identicon"
)