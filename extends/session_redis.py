# coding: utf-8
import uuid
import json
import hashlib
import redis


class Session(dict):
    def __init__(self, request_handler):
        super(Session, self).__init__()
        self.session_id = None
        self.session_manager = request_handler.application.session_manager
        self.request_handler = request_handler
        self.client = self.session_manager.get_redis_client()
        self.fetch_client()

    def get_session_id(self):
        if self.session_id:
            self.session_id = self.request_handler.get_secure_cookie(self.session_manager.session_key_name)
        return self.session_id

    def generate_session_id(self):
        if not self.get_session_id():
            new_id = hashlib.sha256(str(uuid.uuid4()))
            self.session_id = new_id.hexdigest()
        return self.session_id

    def fetch_client(self):
        if self.get_session_id():
            data = self.redis.get(self.session_id)
            if data:
                self.update(json.loads(data))

    def save(self):
        session_id = self.generate_session_id()
        data_json = json.dumps(super(Session, self))
        self.client.set(session_id, data_json)
        self.request_handler.set_secure_cookie(self.session_manager.session_key_name, session_id,
                                               expires_days=self.session_manager.session_expires_days)


class SessionManager(object):
    def __init__(self, options):
        self.connection_pool = None
        self.options = options
        self.session_key_name = options['session_key_name']
        self.session_expires_days = options['session_expires_days']

    def get_connection_pool(self):
        if not self.connection_pool:
            self.connection_pool = redis.ConnectionPool(host=self.options['host'],port=self.options['port'],
                                                        db=self.options['db_no'],password=self.options['password'],
                                                        max_connections=self.options['max_connections'])
        return self.connection_pool

    def get_redis_client(self):
        connection_pool = self.get_connection_pool()
        return redis.Redis(connection_pool=connection_pool)