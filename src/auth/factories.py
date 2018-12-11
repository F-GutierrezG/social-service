from flask import current_app
from .authenticators import MockAuthenticator, Authenticator


class AuthenticatorFactory:
    @staticmethod
    def get_instance():
        if current_app.config['USERS_SERVICE_MOCK']:
            return MockAuthenticator.get_instance()
        return Authenticator()
