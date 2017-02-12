# coding=utf-8
import logging
import re

from sqlalchemy.orm import joinedload, undefer
from model.models import Article, Source
from model.search_params.article_params import ArticleSearchParams
from . import BaseService

logger = logging.getLogger(__name__)


class ArticleService(object):
    MARKDOWN_REG = "[\\\`\*\_\[\]\#\+\-\!\>\s]";
    SUMMARY_LIMIT = 100;

    @staticmethod
    def page_articles(db_session, pager, search_params):
        query = db_session.query(Article)
        if search_params:
            if search_params.show_summary:
                query = query.options(undefer(Article.summary))
            if search_params.show_content:
                query = query.options(undefer(Article.content))
            if search_params.show_source:
                query = query.options(joinedload(Article.source))
            if search_params.show_article_type:
                query = query.options(joinedload(Article.articleType).load_only("id", "name"))
            if search_params.order_mode == ArticleSearchParams.ORDER_MODE_CREATE_TIME_DESC:
                query = query.order_by(Article.create_time.desc())
            if search_params.source_id:
                query = query.filter(Article.source_id==search_params.source_id)
            if search_params.articleType_id:
                query = query.filter(Article.articleType_id==search_params.articleType_id)
        pager = BaseService.query_pager(query, pager)
        if pager.result:
            if search_params.show_comments_count:
                for article in pager.result:
                    article
                    article.fetch_comments_count()
        return pager

    @staticmethod
    def add_article(db_session, article):
        try:
            summary = article["summary"].strip() if article["summary"] else None
            if not summary:
                summary = ArticleService.get_core_content(article["content"], ArticleService.SUMMARY_LIMIT)
            article_to_add = Article(title=article["title"], content=article["content"],
                                     summary=summary, articleType_id=article["articleType_id"],
                                     source_id=article["source_id"])
            db_session.add(article_to_add)
            db_session.commit()
            return article_to_add
        except Exception, e:
            logger.exception(e)
        return None

    @staticmethod
    def get_core_content(content, limit=0):
        core_content = re.sub(ArticleService.MARKDOWN_REG, '', content)
        if limit > 0:
            return core_content[:limit]
        return core_content

    @staticmethod
    def get_count(db_session):
        article_count = db_session.query(Article).count()
        return article_count

    # article_sources
    @staticmethod
    def get_article_sources(db_session):
        article_sources = db_session.query(Source).all()
        if article_sources:
            for source in article_sources:
                source.fetch_articles_count()
        return article_sources
