from functools import wraps
from flask import request, jsonify, current_app

from project.services import AuthService


def forbidden(message='forbidden'):
    return jsonify({'message': message}), 403


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']


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
        self.user = None

    @staticmethod
    def get_instance():
        if MockAuthenticator.instance is None:
            MockAuthenticator.instance = MockAuthenticator()
        return MockAuthenticator.instance

    def authenticate(self, f, *args, **kwargs):
        return f(self.user, *args, **kwargs)

    def set_user(self, user_data):
        self.user = User(user_data)


class AuthenticatorFactory:
    @staticmethod
    def get_instance():
        if current_app.config['USERS_SERVICE_MOCK']:
            return MockAuthenticator.get_instance()
        return Authenticator()


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return AuthenticatorFactory.get_instance().authenticate(
            f, *args, **kwargs)
    return decorated_function
