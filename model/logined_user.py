# coding=utf-8


class LoginUser(dict):
    def __init__(self):
        super(LoginUser, self).__init__()
        # self['name'] = None
        # self['avatar'] = None
        # self['messages'] = None

    def __init__(self, user):
        if isinstance(user, dict):
            super(LoginUser, self).__init__()
            self.update(user)
        else:
            self.__init__()

    def add_message(self, message):
        if 'messages' not in self:
            self['messages'] = [message]
        else:
            self['messages'].append(message)

    def read_messages(self):
        all_messages = self['messages']
        self['messages'] = None
        return all_messages