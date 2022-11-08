from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    need_close = pyqtSignal()
    no_internet_connection = pyqtSignal()
    update_chats = pyqtSignal()