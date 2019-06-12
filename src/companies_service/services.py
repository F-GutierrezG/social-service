import json
import requests

from flask import request, current_app


class CompaniesService:
    def get_company(self, company_id):
        url = '{}/{}'.format(
            current_app.config['COMPANIES_SERVICE_URL'],
            company_id)
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data

    def get_brand(self, brand_id):
        url = '{}/brands/{}'.format(
            current_app.config['COMPANIES_SERVICE_URL'],
            brand_id)
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data

    def get_user_companies(self):
        url = '{0}'.format(
            current_app.config['COMPANIES_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data

    def get_company_users(self, company_id):
        url = '{}/{}/users'.format(
            current_app.config['COMPANIES_SERVICE_URL'],
            company_id)
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data


class Response:
    status_code = 200


class CompaniesServiceMock:
    instance = None

    def __init__(self):
        self.clear()

    def clear(self):
        self.company = None
        self.brand = None
        self.companies = []
        self.users_companies = {}
        self.user = None
        self.users = []
        return CompaniesServiceMock.instance

    def set_user(self, user):
        self.user = user

    @staticmethod
    def get_instance():
        if CompaniesServiceMock.instance is None:
            CompaniesServiceMock.instance = CompaniesServiceMock()
        return CompaniesServiceMock.instance

    def set_company(self, company):
        self.company = company

    def set_brand(self, brand):
        self.brand = brand

    def add_company(self, company):
        self.companies.append(company)

    def add_user_to_company(self, user, company):
        if user['id'] not in self.users_companies:
            self.users_companies[user['id']] = []

        self.users_companies[user['id']].append(company)

    def get_user_companies(self):
        return Response(), list(map(
                lambda company: {'id': company['id']},
                self.users_companies[self.user['id']]))

    def set_users(self, users):
        self.users = users

    def get_company(self, company_id):
        return Response(), self.company

    def get_brand(self, brand_id):
        return Response(), self.brand

    def get_company_users(self, company_id):
        users = []
        for user in self.users:
            users.append(user)
        return Response(), users
