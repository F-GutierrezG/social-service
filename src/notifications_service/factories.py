from flask import current_app
from .services import NotificationsServiceMock, NotificationsService


class NotificationsServiceFactory:
    def get_instance():
        if current_app.config['NOTIFICATIONS_SERVICE_MOCK']:
            return NotificationsServiceMock.get_instance()
        return NotificationsService()
