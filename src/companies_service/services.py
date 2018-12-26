import json
import requests

from flask import request, current_app

from companies_service.models import Company


class CompaniesService:
    def get_user_companies(self):
        url = '{0}/companies'.format(
            current_app.config['COMPANIES_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data


class CompaniesServiceMock:
    instance = None

    def __init__(self):
        self.clear()

    def clear(self):
        self.companies = []
        self.users_companies = {}
        self.user = None
        return CompaniesServiceMock.instance

    def set_user(self, user):
        self.user = user

    @staticmethod
    def get_instance():
        if CompaniesServiceMock.instance is None:
            CompaniesServiceMock.instance = CompaniesServiceMock()
        return CompaniesServiceMock.instance

    def add_company(self, company):
        self.companies.append(company)

    def add_user_to_company(self, user, company):
        if user['id'] not in self.users_companies:
            self.users_companies[user['id']] = []

        self.users_companies[user['id']].append(company)

    def get_user_companies(self):
        return list(map(
                lambda company: {'id': company['id']},
                self.users_companies[self.user['id']]))
