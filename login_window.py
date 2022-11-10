import time
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
)

from messenger_api import MessengerAPI, no_error
from my_signals import Signals


class LoginWindow(QWidget):
    @no_error
    def __init__(self, application):
        super().__init__()

        self.need_update_lbl_info = False
        self.program_close = False
        self.application = application

        self.signal = Signals()
        self.signal.need_close.connect(lambda: [setattr(self, 'program_close', True), self.close()])

        self.setWindowTitle('Вход')
        self.setFixedWidth(300)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.lbl_title = QLabel("Вход")
        self.lbl_title.setFont(
            QFont(
                self.lbl_title.font().family(),
                self.lbl_title.font().pointSize() * 2
            )
        )
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setContentsMargins(0, 0, 0, 20)

        self.vbox.addWidget(self.lbl_title)

        self.hbox_login = QHBoxLayout()
        self.vbox.addLayout(self.hbox_login)

        self.lbl_login = QLabel("Логин: ")
        self.hbox_login.addWidget(self.lbl_login)

        self.edt_login = QLineEdit()
        self.edt_login.returnPressed.connect(lambda: Thread(target=self.on_click).start())
        self.hbox_login.addWidget(self.edt_login)

        self.hbox_password = QHBoxLayout()
        self.vbox.addLayout(self.hbox_password)

        self.lbl_password = QLabel("Пароль: ")
        self.hbox_password.addWidget(self.lbl_password)

        self.edt_password = QLineEdit()
        self.edt_password.setEchoMode(QLineEdit.Password)
        self.edt_password.returnPressed.connect(lambda: Thread(target=self.on_click).start())
        self.hbox_password.addWidget(self.edt_password)

        self.lbl_info = QLabel()
        self.vbox.addWidget(self.lbl_info)
        self.lbl_info.setVisible(False)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(lambda: Thread(target=self.on_click).start())
        self.vbox.addWidget(self.btn_login)

        self.btn_sign_up = QPushButton("Регистрация")
        self.btn_sign_up.clicked.connect(self.application.from_login_open_sign_up)
        self.vbox.addWidget(self.btn_sign_up)

        self.setFixedHeight(200)

    @no_error
    def update_lbl_info(self):
        n = 0
        self.setFixedHeight(220)
        h = self.height()
        self.lbl_info.setVisible(True)
        self.need_update_lbl_info = True

        while self.need_update_lbl_info:
            time.sleep(0.1)
            n = (n + 1) % 5
            self.lbl_info.setText("Входим" + '. ' * n)
        self.lbl_info.setVisible(False)
        self.setFixedHeight(200)

    @no_error
    def on_click(self):
        login = self.edt_login.text()
        password = self.edt_password.text()
        if login != '' and password != '':
            Thread(target=self.update_lbl_info).start()
            t = time.time()
            data = MessengerAPI.get_token(login, password)
            while time.time() < t + 1:
                pass
            self.need_update_lbl_info = False
            if data['code'] == -1:
                QMessageBox(QMessageBox.Warning, "Ошибка", "Нет интернет-соединения").exec()
            elif data['code'] == MessengerAPI.CODE_SUCCESS:
                self.application.callback_authed(login, password, data['token'])
                self.signal.need_close.emit()
            elif data['code'] == MessengerAPI.CODE_INCORRECT_PASSWORD:
                QMessageBox(QMessageBox.Warning, "Ошибка", "Неверный пароль").exec()
            elif data['code'] == MessengerAPI.CODE_USER_NOT_FOUND:
                QMessageBox(QMessageBox.Warning, "Ошибка", "Пользователь не найден").exec()

    def closeEvent(self, a0):
        if not self.program_close:
            exit(0)