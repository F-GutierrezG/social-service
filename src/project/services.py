import json
import requests

from flask import request, current_app


class AuthService:
    def status(self, token):
        url = '{0}/auth/status'.format(current_app.config['USERS_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data


class UsersServiceFactory:
    def get_instance():
        if current_app.config['USERS_SERVICE_MOCK']:
            return UsersServiceMock.get_instance()
        return UsersService()


class UsersService:
    def filter_by_id(self, ids=[]):
        url = '{0}/users/{1}'.format(
            current_app.config['USERS_SERVICE_URL'], ','.join(ids))
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data


class UsersServiceMock:
    instance = None

    def __init__(self):
        self.users = []

    @staticmethod
    def get_instance():
        if UsersServiceMock.instance is None:
            UsersServiceMock.instance = UsersServiceMock()
        return UsersServiceMock.instance

    def set_users(self, users):
        self.users = users

    def filter_by_id(self, ids=[]):
        return self.users
