from flask import current_app
from .services import CompaniesServiceMock, CompaniesService


class CompaniesServiceFactory:
    def get_instance():
        if current_app.config['COMPANIES_SERVICE_MOCK']:
            return CompaniesServiceMock.get_instance()
        return CompaniesService()
