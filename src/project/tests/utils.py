import random
import string
from sqlalchemy.sql import func

from users_service.factories import UsersServiceFactory
from companies_service.factories import CompaniesServiceFactory

from project import db
from project.models import Publication, Category


def add_publication(
        company_id=1, brand_id=1, status=Publication.Status.PENDING):
    publication = Publication(
        company_id=company_id,
        brand_id=brand_id,
        created_by=1,
        datetime=func.now(),
        title=random_string(),
        category=random_string(),
        subcategory=random_string(),
        status=status)

    db.session.add(publication)
    db.session.commit()

    companies_service = CompaniesServiceFactory.get_instance().clear()
    companies_service.set_company({
        'id': company_id,
        'identifier': random_string(),
        'name': random_string()})
    companies_service.set_brand({
        'id': brand_id,
        'name': random_string()})

    return publication


def add_admin():
    return __add_user(admin=True)


def add_user():
    return __add_user()


def add_company():
    companies_service = CompaniesServiceFactory.get_instance()
    company = {
        'id': random.randint(0, 100000)
    }
    companies_service.add_company(company)
    return company


def add_brand():
    companies_service = CompaniesServiceFactory.get_instance()
    brand = {
        'id': random.randint(0, 100000)
    }
    companies_service.add_company(brand)
    return brand


def add_category():
    category = Category(name=random_string())

    db.session.add(category)
    db.session.commit()

    return category


def __add_user(admin=False):
    users_service = UsersServiceFactory.get_instance()
    user = {
        'id': random.randint(0, 100000),
        'first_name': random_string(),
        'last_name': random_string(),
        'email': '{}@test.com'.format(random_string),
        'admin': admin,
        'hash': random_string(32)
    }
    users_service.add_user(user)
    return user


def random_string(length=32):
    return ''.join(
        [random.choice(
            string.ascii_letters + string.digits
        ) for n in range(length)]
    )
