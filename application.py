import sys

from PyQt5.QtWidgets import QApplication

from login_window import LoginWindow
from messenger_api import no_error
from sign_up_window import SignUpWindow
from chats_window import ChatsWindow


@no_error
class Application:
    def __init__(self):
        self.token = None
        self.login = None
        self.password = None

        self.q_app = QApplication(sys.argv)

        self.login_window = LoginWindow(self)
        self.sign_up_window = SignUpWindow(self)
        self.chats_window = ChatsWindow(self)

    def run(self):
        self.login_window.show()

        self.q_app.exec()

        if self.token is None or self.login is None or self.password is None:
            print('token or login or password is None')
            exit(1)

        self.chats_window.run()

        self.q_app.exec()
        exit(0)

    def callback_authed(self, login, password, token):
        self.token = token
        self.login = login
        self.password = password

    def go_to_login(self):
        self.chats_window.need_load_chats = False
        self.chats_window.hide()
        self.run()

    def from_login_open_sign_up(self):
        self.sign_up_window.show()
        self.login_window.hide()

    def from_sign_up_open_login(self):
        self.sign_up_window.hide()
        self.login_window.show()