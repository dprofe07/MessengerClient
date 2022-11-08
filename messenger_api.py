import requests
import urllib3.exceptions


class MessengerAPI:
    # noinspection HttpUrlsUsage
    URL = 'http://91.204.57.48:8003/api'

    CODE_SUCCESS = 0
    CODE_NOT_A_CHAT_MEMBER = 1
    CODE_CHAT_NOT_FOUND = 2
    CODE_FORBIDDEN_SYMBOLS_IN_LOGIN = 3
    CODE_USER_NOT_FOUND = 4
    CODE_INCORRECT_PASSWORD = 5
    CODE_INCORRECT_SYNTAX = 6
    CODE_USER_ALREADY_EXISTS = 7
    CODE_DO_NOT_NEED_UPDATE = 8

    @staticmethod
    def get_token(login, password):
        try:
            req = requests.get(MessengerAPI.URL + '/get-token', {'login': login, 'password': password})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()

    @staticmethod
    def get_chats(token):
        try:
            req = requests.get(MessengerAPI.URL + '/get-chats', {'token': token})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()

    @staticmethod
    def get_messages(token, chat_id):
        try:
            req = requests.get(MessengerAPI.URL + '/chat', {'token': token, 'chat-id': chat_id})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()

    @staticmethod
    def send_message(token, chat_id, text):
        try:
            req = requests.get(MessengerAPI.URL + '/send-message', {'token': token, 'chat-id': chat_id, 'text': text})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()

    @staticmethod
    def sign_up(login, password, keyword):
        try:
            req = requests.get(MessengerAPI.URL + '/signup', {'login': login, 'password': password, 'keyword': keyword})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()

    @staticmethod
    def create_chat(token, name, members, password):
        try:
            req = requests.get(MessengerAPI.URL + '/create-chat', {'token': token, 'password': password, 'members': members, 'name': name})
        except requests.exceptions.ConnectionError:
            return {'code': -1}
        return req.json()