from flask import current_app
from .services import UsersServiceMock, UsersService


class UsersServiceFactory:
    def get_instance():
        if current_app.config['USERS_SERVICE_MOCK']:
            return UsersServiceMock.get_instance()
        return UsersService()
