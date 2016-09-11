# coding=utf-8


database_config = dict(
    engine_config='postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog',
    sql_echo=True,
)

config = dict(
    debug=True,
    compress_response=True,
    xsrf_cookies=True,
    cookie_secret="kjsdhfweiofjhewnfiwehfneiwuhniu",
    login_url="/auth/login",
    server_port=8888,
    database=database_config,
)