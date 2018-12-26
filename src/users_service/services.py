import json
import requests

from flask import request, current_app


class UsersService:
    def filter_by_ids(self, ids=[]):
        url = '{0}/{1}'.format(
            current_app.config['USERS_SERVICE_URL'], ','.join(ids))
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data

    def get_admin_users(self):
        url = '{0}/admins'.format(
            current_app.config['USERS_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data


class UsersServiceMock:
    instance = None

    def __init__(self):
        self.clear()

    def clear(self):
        self.users = []

    @staticmethod
    def get_instance():
        if UsersServiceMock.instance is None:
            UsersServiceMock.instance = UsersServiceMock()
        return UsersServiceMock.instance

    def set_users(self, users):
        self.users = users

    def add_user(self, user):
        self.users.append(user)

    def filter_by_ids(self, ids=[]):
        users = []
        for user in self.users:
            if user['id'] in ids:
                users.append(user)
        return users

    def get_admin_users(self):
        users = []
        for user in self.users:
            if user['admin']:
                users.append(user)
        return users
