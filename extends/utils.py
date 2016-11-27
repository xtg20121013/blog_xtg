import json
from sqlalchemy.ext.declarative import DeclarativeMeta


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value, cls=AlchemyEncoder)
                    data[field] = value
                except TypeError:
                    data[field] = None
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
            raise AttributeError(key)