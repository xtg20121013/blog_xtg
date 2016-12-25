# coding: utf-8
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
DbBase = declarative_base()


class DbInit(object):
    created_at = Column(DateTime, default=datetime.now)


class User(DbBase,DbInit):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(128))
    avatar = Column(String(128))

    def verify_password(self, password):
        return self.password == password


class Menu(DbBase):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    types = relationship('ArticleType', backref='menu', lazy='dynamic')
    order = Column(Integer, default=0, nullable=False)

    def fetch_all_types(self):
        self.all_types = self.types.all()

    def __repr__(self):
        return '<Menu %r>' % self.name


class ArticleTypeSetting(DbBase):
    __tablename__ = 'articleTypeSettings'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    protected = Column(Boolean, default=False)
    hide = Column(Boolean, default=False)
    types = relationship('ArticleType', backref='setting', lazy='dynamic')

    @staticmethod
    def return_setting_hide():
        return [(2, u'公开'), (1, u'隐藏')]

    def __repr__(self):
        return '<ArticleTypeSetting %r>' % self.name


class ArticleType(DbBase):
    __tablename__ = 'articleTypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    introduction = Column(Text, default=None)
    articles = relationship('Article', backref='articleType', lazy='dynamic')
    menu_id = Column(Integer, ForeignKey('menus.id'), default=None)
    setting_id = Column(Integer, ForeignKey('articleTypeSettings.id'))

    @property
    def is_protected(self):
        if self.setting:
            return self.setting.protected
        else:
            return False

    @property
    def is_hide(self):
        if self.setting:
            return self.setting.hide
        else:
            return False
    # if the articleType does not have setting,
    # its is_hie and is_protected property will be False.

    def __repr__(self):
        return '<Type %r>' % self.name


class Source(DbBase):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    articles = relationship('Article', backref='source', lazy='dynamic')

    def fetch_articles_count(self):
        self.articles_count = self.articles.count()

    def __repr__(self):
        return '<Source %r>' % self.name


class Follow(DbBase):
    __tablename__ = 'follows'
    follower_id = Column(Integer, ForeignKey('comments.id'),
                           primary_key=True)
    followed_id = Column(Integer, ForeignKey('comments.id'),
                         primary_key=True)


class Comment(DbBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    author_name = Column(String(64))
    author_email = Column(String(64))
    article_id = Column(Integer, ForeignKey('articles.id'))
    disabled = Column(Boolean, default=False)
    comment_type = Column(String(64), default='comment')
    reply_to = Column(String(128), default='notReply')
    followed = relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def is_reply(self):
        if self.followed.count() == 0:
            return False
        else:
            return True
    # to confirm whether the comment is a reply or not

    def followed_name(self):
        if self.is_reply():
            return self.followed.first().followed.author_name

class Article(DbBase):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), unique=True)
    content = Column(Text)
    summary = Column(Text)
    create_time = Column(DateTime, index=True, default=datetime.now)
    update_time = Column(DateTime, index=True, default=datetime.now)
    num_of_view = Column(Integer, default=0)
    articleType_id = Column(Integer, ForeignKey('articleTypes.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    comments = relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def add_view(session, article):
        article.num_of_view += 1
        session.add(article)
        session.commit()

    def __repr__(self):
        return '<Article %r>' % self.title


class BlogInfo(DbBase):
    __tablename__ = 'blog_info'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    signature = Column(Text)
    navbar = Column(String(64))


class Plugin(DbBase):
    __tablename__ = 'plugins'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), unique=True)
    note = Column(Text, default='')
    content = Column(Text, default='')
    order = Column(Integer, index=True, default=0)
    disabled = Column(Boolean, default=False)

    def __repr__(self):
        return '<Plugin %r>' % self.title


class BlogView(DbBase):
    __tablename__ = 'blog_view'
    id = Column(Integer, primary_key=True)
    num_of_view = Column(BigInteger, default=0)

    @staticmethod
    def add_view(session):
        view = BlogView.query.first()
        view.num_of_view += 1
        session.add(view)
        session.commit()
