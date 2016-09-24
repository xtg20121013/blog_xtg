# coding=utf-8


class Pager:
    def __init__(self):
        self.pageNo = 1
        self.pageSize = 15
        self.totalPage = 1
        self.totalCount = 0

    def __init__(self, request):
        self.__init__()
        self.pageNo = request.get_argument("pageNo", self.pageNo)
        self.pageSize = request.get_argument("pageSize", self.pageSize)
