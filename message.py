class Message:
    def __init__(self, sender_login, text, time):
        self.sender_login = sender_login
        self.text = text
        self.time = time

    @staticmethod
    def from_dict(dct):
        return Message(dct['sender_login'], dct['text'], dct['time'])
