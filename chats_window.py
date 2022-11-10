import time
from threading import Thread

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QListWidget, QListWidgetItem
)

from chat import Chat
from messenger_api import MessengerAPI, no_error
from my_signals import Signals


class ChatsWindow(QWidget):
    @no_error
    def __init__(self, application):
        super().__init__()

        self.application = application
        self.need_load_chats = True
        self.update_chats_time = 0
        self.chats = []
        self.current_chat_pos = -1
        self.signal = Signals()

        self.signal.no_internet_connection.connect(self.no_internet_connection)
        self.signal.update_chats.connect(self.update_chats_ui)

        self.setWindowTitle('Чаты')

        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        self.vboxL = QVBoxLayout()
        self.hbox.addLayout(self.vboxL)

        self.lbl_my_login = QLabel()
        self.vboxL.addWidget(self.lbl_my_login)

        self.lst_chats = QListWidget()
        self.lst_chats.currentRowChanged.connect(self.on_chat_click)
        self.vboxL.addWidget(self.lst_chats)

        self.hbox_add_dialog = QHBoxLayout()
        self.vboxL.addLayout(self.hbox_add_dialog)

        self.edt_companion_login = QLineEdit()
        self.edt_companion_login.setPlaceholderText('Логин себеседника')
        self.edt_companion_login.returnPressed.connect(self.add_dialog)
        self.hbox_add_dialog.addWidget(self.edt_companion_login)

        self.btn_add_dialog = QPushButton("Создать диалог")
        self.btn_add_dialog.clicked.connect(self.add_dialog)
        self.hbox_add_dialog.addWidget(self.btn_add_dialog)

        self.vboxR = QVBoxLayout()
        self.hbox.addLayout(self.vboxR)

        self.lbl_current_chat = QLabel("Выберите чат")
        self.vboxR.addWidget(self.lbl_current_chat)

        self.lst_messages = QListWidget()
        self.vboxR.addWidget(self.lst_messages)

        self.hbox_new_message = QHBoxLayout()
        self.vboxR.addLayout(self.hbox_new_message)

        self.edt_msg = QLineEdit()
        self.edt_msg.setPlaceholderText('Сообщение. . .')
        self.edt_msg.returnPressed.connect(self.send_message)
        self.hbox_new_message.addWidget(self.edt_msg)

        self.btn_send = QPushButton(">")
        self.btn_send.clicked.connect(self.send_message)
        self.hbox_new_message.addWidget(self.btn_send)

        self.setMinimumSize(700, 400)

    @no_error
    def run(self):
        self.lbl_my_login.setText(f"Вы вошли как {self.application.login}")

        self.show()
        Thread(target=self.load_chats).start()

    @no_error
    def add_dialog(self):
        login = self.edt_companion_login.text()
        self.edt_companion_login.setText('')
        if login == '' or ';' in login:
            return
        res = MessengerAPI.create_dialog(self.application.token, login)
        if res['code'] == MessengerAPI.CODE_SUCCESS:
            self.update_chats_time = 0
        elif res['code'] == MessengerAPI.CODE_USER_NOT_FOUND:
            QMessageBox(QMessageBox.Warning, 'Ошибка', f'Пользователь с логином {login} не найден').exec()

    @no_error
    def update_chats_ui(self):
        self.lst_chats.clear()

        for chat in self.chats:
            item = QListWidgetItem(chat.get_name_with_members())
            self.lst_chats.addItem(item)

        self.lst_chats.setCurrentRow(self.current_chat_pos)

    @no_error
    def no_internet_connection(self):
        print('No internet connection')
        self.lbl_my_login.setText(self.lbl_my_login.text() + '\nНет интернета!')

    @no_error
    def send_message(self, e=None):
        text = self.edt_msg.text()
        self.edt_msg.setText('')
        res = MessengerAPI.send_message(self.application.token, self.chats[self.current_chat_pos].id, text)
        if res['code'] == -1:
            QMessageBox(QMessageBox.Warning, "Ошибка", "Нет интернет-соединения").exec()
        elif res['code'] != 0:
            QMessageBox(QMessageBox.Warning, "Ошибка", f'Не отправляется сообщение с кодом {res["code"]}').show()
        else:
            self.update_chats_time = 0

    @no_error
    def load_chats(self):
        while self.need_load_chats:
            if time.time() < self.update_chats_time + 10:
                time.sleep(0.1)
                continue
            self.update_chats_time = time.time()

            chat_id = -1
            if self.current_chat_pos != -1:
                chat_id = self.chats[self.current_chat_pos].id

            json = MessengerAPI.get_chats(self.application.token)
            if json['code'] == -1:
                self.signal.no_internet_connection.emit()
                continue
            if json['code'] != 0:
                QMessageBox(
                    QMessageBox.Icon.Critical,
                    "Ошибка",
                    "Произошла ошибка. Вероятно вы вышли из аккаунта на всех устройствах."
                    " Если это не так, свяжитесь с создателем мессенджера, написав в личные "
                    f"сообщения пользователю SYSTEM. Код ошибки: {json['code']}"
                )
                self.application.go_to_login()

            self.lbl_my_login.setText(f'Вы вошли как {self.application.login}')

            self.chats = [
                Chat.from_dict(self.application, i)
                for i in json['chats']
            ]

            self.current_chat_pos = -1

            if chat_id != -1:
                for i in range(len(self.chats)):
                    if self.chats[i].id == chat_id:
                        self.current_chat_pos = i
                        break

            self.signal.update_chats.emit()

    @no_error
    def on_chat_click(self, pos):
        if pos == -1:
            return
        try:
            self.lbl_current_chat.setText(self.chats[pos].show_name)
        except (KeyError, IndexError) as e:
            print(type(e))
            return

        self.current_chat_pos = pos

        self.lst_messages.clear()
        for msg in self.chats[pos].messages:
            item = QListWidgetItem(f"[{msg.sender_login}] {msg.text}")
            self.lst_messages.addItem(item)

        self.lst_messages.scrollToBottom()

    def closeEvent(self, a0):
        self.need_load_chats = False
        time.sleep(0.2)
        exit(0)