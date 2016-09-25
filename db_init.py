# coding=utf-8
from model.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

ENGINE_CONFIG = config['database']['engine_url']
engine = create_engine(ENGINE_CONFIG, **config['database']['engine_setting'])
db = sessionmaker(bind=engine)
session = db()


def insert_admin(email, username, password):
    user = User(email=email, username=username, password=password)
    session.add(user)


def insert_menus():
    menus = [u'Web开发', u'数据库', u'网络技术', u'爱生活，爱自己',
             u'Linux世界', u'开发语言']
    for i in range(0, len(menus)):
        name = menus[i]
        menu = Menu(name=name)
        session.add(menu)
        session.commit()
        menu.order = i + 1;
        session.add(menu)


def insert_system_setting():
    system = ArticleTypeSetting(name='system', protected=True, hide=True)
    session.add(system)


def insert_default_settings():
    system_setting = ArticleTypeSetting(name='system', protected=True, hide=True)
    common_setting = ArticleTypeSetting(name='common', protected=False, hide=False)
    session.add(system_setting)
    session.add(common_setting)


def insert_system_articleType():
    articleType = ArticleType(name=u'未分类',
                              introduction=u'系统默认分类，不可删除。',
                              setting= session.query(ArticleTypeSetting).filter_by(protected=True).first()
                              )
    session.add(articleType)


def insert_articleTypes():
    articleTypes = ['Python', 'Java', 'JavaScript', 'Django',
                    'CentOS', 'Ubuntu', 'MySQL', 'Redis',
                    u'Linux成长之路', u'Linux运维实战', u'其它',
                    u'思科网络技术', u'生活那些事', u'学校那些事',
                    u'感情那些事', 'Flask']
    for name in articleTypes:
        articleType = ArticleType(name=name,
                                  setting=ArticleTypeSetting(name=name))
        session.add(articleType)


def insert_sources():
    sources = (u'原创',
               u'转载',
               u'翻译')
    for s in sources:
        source = session.query(Source).filter_by(name=s).first()
        if source is None:
            source = Source(name=s)
        session.add(source)


def insert_blog_info():
    blog_mini_info = BlogInfo(title=u'开源博客系统Blog_mini',
                              signature=u'让每个人都轻松拥有可管理的个人博客！— By xpleaf',
                              navbar='inverse')
    session.add(blog_mini_info)


def insert_system_plugin():
    plugin = Plugin(title=u'博客统计',
                    note=u'系统插件',
                    content='system_plugin', order=1)
    session.add(plugin)


def insert_view():
    view = BlogView(num_of_view=0)
    session.add(view)


if __name__ == '__main__':
    DbBase.metadata.create_all(engine)
    # step_1:insert basic blog info
    insert_blog_info()
    # step_2:insert admin account
    insert_admin(email='blog_mini@163.com', username='blog_mini', password='blog_mini')
    # step_3:insert system default setting
    insert_system_setting()
    # step_4:insert default article sources
    insert_sources()
    # step_5:insert default articleType
    insert_system_articleType()
    # step_6:insert system plugin
    insert_system_plugin()
    # step_7:insert blog view
    insert_view()
    session.commit()