# coding=utf-8
from extends.utils import Dict


class Pager(Dict):

    DEFAULT_PAGE_SIZE = 10

    def __init__(self, request):
        self.pageNo = int(request.get_argument("pageNo", 1))
        self.pageSize = int(request.get_argument("pageSize", Pager.DEFAULT_PAGE_SIZE))
        self.totalPage = 1
        self.totalCount = 0
        self.result = []

    def build_query(self, query):
        limit = self.pageSize
        if self.pageNo < 0:
            self.pageNo = self.pageNo + self.totalPage + 1
        offset = (self.pageNo-1)*self.pageSize if self.pageNo > 0 else 0
        query = query.limit(limit).offset(offset)
        return query

    def set_total_count(self, count):
        self.totalCount = count
        if count > 0:
            self.totalPage = (count+self.pageSize-1) / self.pageSize

    def set_result(self, result):
        if result:
            self.result = result

    def has_prev(self):
        return self.pageNo > 1

    def has_next(self):
        return self.pageNo < self.totalPage

    def build_url(self, url, page_no, params):
        if '?' in url:
            parts = url.split('?', 1)
            url = parts[0]
            params = parts[1]+"&"+params
        if page_no < 1:
            page_no = 0
        if page_no > self.totalPage:
            page_no = self.totalPage
        url = "{0}?pageNo={1}".format(url, page_no)
        if self.pageSize != Pager.DEFAULT_PAGE_SIZE:
            url += "&pageSize={0}".format(self.pageSize)
        if params:
            url += "&{0}".format(params)
        return url
