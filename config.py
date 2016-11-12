# coding=utf-8

redis_session_config = dict(
    db_no=0,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
    session_key_name="TR_SESSION_ID",
    session_expires_days=7,
)

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
)

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
)