import io
import json
import random
import datetime
import unittest

from auth.factories import AuthenticatorFactory
from companies_service.factories import CompaniesServiceFactory

from project.tests.utils import (
    random_string, add_publication, add_admin, add_user, add_company)

from project.tests.base import BaseTestCase
from project.models import Publication


class TestListPublications(BaseTestCase):
    """Tests for list publications"""

    def test_list_publications(self):
        """Ensure list publications behaves correctly"""
        publications_qty = random.randint(5, 10)

        self.assertEqual(Publication.query.count(), 0)

        for i in range(0, publications_qty):
            add_publication()

        admin = add_admin()
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(admin)

        with self.client:
            response = self.client.get(
                '/social/publications',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Publication.query.count(), publications_qty)
            self.assertEqual(len(response_data), publications_qty)

    def test_list_publications_by_company(self):
        """Ensure list publications behaves correctly"""
        publications_company_1_qty = random.randint(5, 10)
        publications_company_2_qty = random.randint(5, 10)

        self.assertEqual(Publication.query.count(), 0)

        company_service = CompaniesServiceFactory.get_instance().clear()
        company1 = add_company()
        company2 = add_company()

        for i in range(0, publications_company_1_qty):
            add_publication(company_id=company1['id'])

        for i in range(0, publications_company_2_qty):
            add_publication(company_id=company2['id'])

        self.assertEqual(
            Publication.query.count(),
            publications_company_1_qty + publications_company_2_qty)

        user = add_user()
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(user)
        company_service.set_user(user)

        company_service.add_user_to_company(user, company1)

        with self.client:
            response = self.client.get(
                '/social/publications',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                Publication.query.count(),
                publications_company_1_qty + publications_company_2_qty)
            self.assertEqual(len(response_data), publications_company_1_qty)


class TestCreatePublication(BaseTestCase):
    """Tests for create publications"""

    def test_create_publication(self):
        """Ensure create publications behaves correctly"""
        self.assertEqual(Publication.query.count(), 0)

        user = add_user()
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(user)

        current_time = datetime.datetime.today()

        date = '{}-{}-{}'.format(
            current_time.year, current_time.month, current_time.day)
        time = '{}:{}'.format(current_time.hour, current_time.minute)

        data = {
            'company_id': random.randint(0, 1000),
            'date': date,
            'time': time,
            'title': random_string(),
            'message': random_string(256),
            'image': (io.BytesIO(b"abcdef"), 'test.jpg'),
            'social_networks': random_string(),
        }

        with self.client:
            response = self.client.post(
                '/social/publications',
                buffered=True,
                data=data,
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='multipart/form-data'
            )
            # response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(Publication.query.count(), 1)


class TestRejectPublication(BaseTestCase):
    """Tests for reject publications"""

    def test_reject_publication(self):
        """Reject publication behaves correctly"""
        admin = add_admin()
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(admin)

        publication = add_publication()
        data = {
            'message': random_string()
        }

        self.assertEqual(
            Publication.query.filter_by(id=publication.id).first().status,
            Publication.Status.PENDING)

        with self.client:
            response = self.client.put(
                '/social/publications/{}/reject'.format(publication.id),
                data=json.dumps(data),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            # response_data = json.loads(response.data.decode())
            publication = Publication.query.filter_by(
                id=publication.id).first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Publication.query.count(), 1)
            self.assertEqual(publication.status, Publication.Status.REJECTED)
            self.assertEqual(publication.reject_reason, data['message'])


class TestAcceptPublication(BaseTestCase):
    """Tests for accept publications"""

    def test_accept_publication(self):
        """Accept publication behaves correctly"""

        admin = add_admin()
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(admin)

        publication = add_publication()

        self.assertEqual(
            Publication.query.filter_by(id=publication.id).first().status,
            Publication.Status.PENDING)

        with self.client:
            response = self.client.put(
                '/social/publications/{}/accept'.format(publication.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            # response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Publication.query.count(), 1)
            self.assertEqual(
                Publication.query.filter_by(id=publication.id).first().status,
                Publication.Status.ACCEPTED)


if __name__ == '__main__':
    unittest.main()
