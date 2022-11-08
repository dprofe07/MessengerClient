import time
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
)

from messenger_api import MessengerAPI
from my_signals import Signals


class SignUpWindow(QWidget):
    def __init__(self, application):
        super().__init__()

        self.need_update_lbl_login = False
        self.application = application

        self.signal = Signals()
        self.signal.need_close.connect(self.close)

        self.setWindowTitle('Регистрация')
        self.setFixedWidth(300)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.lbl_title = QLabel("Регистрация")
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

        self.hbox_password2 = QHBoxLayout()
        self.vbox.addLayout(self.hbox_password2)

        self.lbl_password2 = QLabel("Повторите пароль: ")
        self.hbox_password2.addWidget(self.lbl_password2)

        self.edt_password2 = QLineEdit()
        self.edt_password2.setEchoMode(QLineEdit.Password)
        self.edt_password2.returnPressed.connect(lambda: Thread(target=self.on_click).start())
        self.hbox_password2.addWidget(self.edt_password2)

        self.hbox_keyword = QHBoxLayout()
        self.vbox.addLayout(self.hbox_keyword)

        self.lbl_keyword = QLabel("Ключевое слово: ")
        self.hbox_keyword.addWidget(self.lbl_keyword)

        self.edt_keyword = QLineEdit()
        self.edt_keyword.setEchoMode(QLineEdit.Password)
        self.edt_keyword.returnPressed.connect(lambda: Thread(target=self.on_click).start())
        self.hbox_keyword.addWidget(self.edt_keyword)

        self.lbl_info = QLabel()
        self.vbox.addWidget(self.lbl_info)
        self.lbl_info.setVisible(False)

        self.btn_sign_up = QPushButton("Зарегистрироваться")
        self.btn_sign_up.clicked.connect(lambda: Thread(target=self.on_click).start())
        self.vbox.addWidget(self.btn_sign_up)

        self.btn_login = QPushButton("Вход")
        self.btn_login.clicked.connect(self.application.from_sign_up_open_login)
        self.vbox.addWidget(self.btn_login)

        self.setFixedHeight(250)

    def update_lbl_info(self):
        n = 0
        self.setFixedHeight(self.height() + 20)
        h = self.height()
        self.lbl_info.setVisible(True)
        self.need_update_lbl_login = True

        while self.need_update_lbl_login:
            time.sleep(0.1)
            n = (n + 1) % 5
            self.lbl_info.setText("Входим" + '. ' * n)
        self.lbl_info.setVisible(False)
        self.setFixedHeight(self.height() - 20)

    def on_click(self):
        login = self.edt_login.text()
        password = self.edt_password.text()
        password2 = self.edt_password2.text()
        keyword = self.edt_keyword.text()
        if ';' in login:
            QMessageBox(QMessageBox.Icon.Warning, "Ошибка", "Нельзя использовать точку с запятой в логине", QMessageBox.Ok).exec()
        if login != '' and password != '' and keyword != '' and password2 == password:
            Thread(target=self.update_lbl_info).start()
            t = time.time()
            data = MessengerAPI.sign_up(login, password, keyword)
            while time.time() < t + 1:
                pass

            self.need_update_lbl_login = False

            if data['code'] == -1:
                QMessageBox(QMessageBox.Icon.Critical, "Ошибка", "Нет интернет-соединения", QMessageBox.Ok).exec()
            elif data['code'] == MessengerAPI.CODE_USER_ALREADY_EXISTS:
                QMessageBox(QMessageBox.Icon.Critical, "Ошибка", "Этот логин уже занят", QMessageBox.Ok).exec()
            elif data['code'] == MessengerAPI.CODE_SUCCESS:
                self.application.callback_authed(login, password, data['token'])
                self.signal.need_close.emit()
