import json
import requests

from flask import request, current_app


class NotificationsService:
    def send(self, data):
        url = '{0}/send'.format(
            current_app.config['NOTIFICATIONS_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer, 'Content-Type': 'application/json'}
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        data = json.loads(response.text)
        return response, data


class Response:
    status_code = 200


class NotificationsServiceMock:
    instance = None

    def __init__(self):
        self.clear()

    def clear(self):
        return NotificationsServiceMock.instance

    @staticmethod
    def get_instance():
        if NotificationsServiceMock.instance is None:
            NotificationsServiceMock.instance = NotificationsServiceMock()
        return NotificationsServiceMock.instance

    def send(self):
        Response(), {}
