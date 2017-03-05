# coding=utf-8
class CommentSearchParams(object):

    ORDER_MODE_CREATE_TIME_ASC = 1
    ORDER_MODE_CREATE_TIME_DESC = 2

    def __init__(self, request):
        self.order_mode = request.get_argument("order_mode", CommentSearchParams.ORDER_MODE_CREATE_TIME_ASC)
        self.article_id = request.get_argument("article_id", None)
        self.show_article_id_title = False
