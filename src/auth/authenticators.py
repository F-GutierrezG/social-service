from flask import request, jsonify
from .models import User
from .services import AuthService


def forbidden(message='forbidden'):
    return jsonify({'message': message}), 403


class Authenticator:
    def authenticate(self, f, *args, **kwargs):
        token = self.__parse_token()

        if token is False:
            return forbidden()

        response, data = self.__do_request(token)
        if response.status_code == 200:
            user = User(data)
            return f(user, *args, **kwargs)
        else:
            return forbidden()

    def __do_request(self, token):
        return AuthService().status(token)

    def __parse_token(self):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return False

        token_parts = auth_header.split(' ')

        if len(token_parts) != 2:
            return False

        return token_parts[1]


class MockAuthenticator:
    instance = None

    def __init__(self):
        self.clear()

    @staticmethod
    def get_instance():
        if MockAuthenticator.instance is None:
            MockAuthenticator.instance = MockAuthenticator()
        return MockAuthenticator.instance

    def clear(self):
        self.user = None
        return self

    def authenticate(self, f, *args, **kwargs):
        if self.user is None:
            return forbidden()
        return f(self.user, *args, **kwargs)

    def set_user(self, user_data):
        self.user = User(user_data)
