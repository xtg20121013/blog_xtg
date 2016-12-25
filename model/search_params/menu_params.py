# coding=utf-8
class MenuSearchParams(object):

    ORDER_MODE_ORDER_ASC = 1

    def __init__(self, request):
        self.order_mode = request.get_argument("order_mode", MenuSearchParams.ORDER_MODE_ORDER_ASC)
