# coding=utf-8
import json
import logging
from sqlalchemy.ext.declarative import DeclarativeMeta

logger = logging.getLogger(__name__)


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class AlchemyEncoder(json.JSONEncoder):

    def __init__(self, dumps_objs=None, *w, **kw):
        super(AlchemyEncoder, self).__init__(*w, **kw)
        if dumps_objs is None:
            dumps_objs = []
        self.dumps_objs = dumps_objs

    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            self.dumps_objs.append(o)
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            fields = [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]
            for field in fields:
                value = o.__getattribute__(field)
                if value and self.dumps_objs and value in self.dumps_objs:
                    continue
                try:
                    json.dumps(value, cls=AlchemyEncoder, dumps_objs=self.dumps_objs)
                    data[field] = value
                except TypeError:
                    pass
            return data
        return json.JSONEncoder.default(self, o)


#  可通过 .attr 访问的dict
class Dict(dict):
    def __getattr__(self, key):
        try:
            if isinstance(self[key], dict):
                return Dict(self[key])
            return self[key]
        except KeyError:
            logger.warning(key+" not in "+str(self))
            return None;

    def __setattr__(self, key, value):
        self[key] = value
