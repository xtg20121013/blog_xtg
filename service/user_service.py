# coding=utf-8
from model.models import User


class UserService:

    @staticmethod
    def get_user(db_session, username):
        return db_session.query(User).filter(User.username == username).first()

    @staticmethod
    def update_user_info(db_session, username, password, user):
        current_user = UserService.get_user(db_session, username)
        if current_user and current_user.password == password:
            if "username" in user:
                current_user.username = user['username']
            if "email" in user:
                current_user.email = user['email']
            db_session.commit()
            return current_user
        else:
            return None

    @staticmethod
    def update_password(db_session, username, old_password, new_password):
        count = db_session.query(User).filter(User.username == username, User.password == old_password)\
            .update({"password":new_password})
        db_session.commit()
        return count