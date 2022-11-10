from message import Message
from messenger_api import MessengerAPI, no_error


@no_error
class Chat:
    def __init__(self, application, id_, name, members, time_last_message=0):
        self.application = application
        self.id = id_
        self.name = name
        self.members = members
        self.time_last_message = time_last_message
        self.messages = []
        self.get_messages()

        if 'DIALOG_BETWEEN' in self.name:
            names = self.name.replace('DIALOG_BETWEEN/', '').split(';')
            if self.application.login in names:
                name = f'Диалог с {names[0] if names[1] == self.application.login else names[1]}'
            else:
                name = f'Диалог между {names[0]} и {names[1]}'
        else:
            name = 'Чат ' + self.name
        self.show_name = name

    def get_messages(self):
        json = MessengerAPI.get_messages(self.application.token, self.id)
        if json['code'] != 0:
            self.messages = []
        else:
            self.messages = [Message.from_dict(i) for i in json['messages']]

    @staticmethod
    def from_dict(application, dct):
        return Chat(application, dct['id'], dct['name'], dct['members'].split(';'), dct.get('time_last_message', 0))

    def get_name_with_members(self):
        return self.show_name + f' [{", ".join(self.members)}]'
