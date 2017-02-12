# coding=utf-8
class ArticleSearchParams(object):

    ORDER_MODE_CREATE_TIME_DESC = 1

    def __init__(self, request):
        self.order_mode = request.get_argument("order_mode", ArticleSearchParams.ORDER_MODE_CREATE_TIME_DESC)
        self.source_id = request.get_argument("source_id", None)
        self.articleType_id = request.get_argument("articleType_id", None)
        self.show_source = True
        self.show_article_type = True
        self.show_summary = False
        self.show_content = False
        self.show_comments_count = False

    def to_url_params(self):
        s = ""
        if self.source_id:
            s = "source_id={0}".format(self.source_id)
        if self.articleType_id:
            if s:
                s += "&"
            s += "articleType_id={0}".format(self.articleType_id)
        return s