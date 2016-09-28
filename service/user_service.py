# coding=utf-8
from model.models import User


class UserService:

    @staticmethod
    def get_user(db_session, username):
        return db_session.query(User).filter(User.username==username).first()