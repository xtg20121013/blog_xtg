# coding=utf-8
class ArticleTypeSearchParams(object):

    ORDER_MODE_ID_DESC = 1

    def __init__(self, request):
        self.order_mode = request.get_argument("order_mode", ArticleTypeSearchParams.ORDER_MODE_ID_DESC)
        self.show_setting = False
        self.show_articles_count = False
