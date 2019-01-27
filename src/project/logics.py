import datetime

from sqlalchemy import or_
from sqlalchemy import func

from companies_service.factories import CompaniesServiceFactory
from notifications_service.factories import NotificationsServiceFactory

from project import db
from project.models import (
    Publication, PublicationSocialNetwork, PublicationTag, Category,
    Subcategory)
from project.serializers import PublicationSerializer, CategorySerializer
from project.uploaders import S3Uploader


class NotFound(Exception):
    pass


class BadRequest(Exception):
    def __init__(self, message):
        self.message = message


class PublicationLogics:
    def get(self, id):
        return Publication.query.filter_by(id=id).first()

    def list(self, user):
        if user.admin is True:
            publications = Publication.query.filter(
                Publication.status != Publication.Status.DELETED)
        else:
            companies_ids = self.__get_user_companies_ids()
            publications = Publication.query.filter(
                Publication.company_id.in_(companies_ids),
                Publication.status != Publication.Status.DELETED)

        return PublicationSerializer.to_array(publications)

    def list_by_company(self, company_id, user):
        if user.admin is True:
            publications = Publication.query.filter(
                Publication.company_id == company_id,
                Publication.status != Publication.Status.DELETED)
        else:
            companies_ids = self.__get_user_companies_ids()
            publications = Publication.query.filter(
                Publication.company_id.in_(companies_ids),
                Publication.company_id == company_id,
                Publication.status != Publication.Status.DELETED)

        return PublicationSerializer.to_array(publications)

    def create(self, data, user):
        mapped_data = self.__map_data(data)

        publication = Publication(**mapped_data)
        publication.social_networks = self.__create_social_networks(data)
        publication.tags = self.__create_tags(data)

        db.session.add(publication)
        db.session.commit()

        self.__add_subcategory(
            company_id=mapped_data['company_id'],
            category=mapped_data['category'],
            subcategory=mapped_data['subcategory'])

        self.__notify_publication(publication, user)

        return PublicationSerializer.to_dict(publication)

    def reject(self, id, message, user):
        publication = Publication.query.filter_by(id=id).first()

        if publication.status == Publication.Status.REJECTED:
            raise BadRequest("already rejected")

        if publication.status == Publication.Status.ACCEPTED:
            raise BadRequest("accepted")

        publication.status = Publication.Status.REJECTED
        publication.reject_reason = message
        publication.updated_by = user.id

        db.session.add(publication)
        db.session.commit()

        self.__notify_publication(publication, user)

        return PublicationSerializer.to_dict(publication)

    def accept(self, id, user):
        publication = Publication.query.filter_by(id=id).first()

        if publication.status == Publication.Status.ACCEPTED:
            raise BadRequest("already rejected")

        if publication.status == Publication.Status.REJECTED:
            raise BadRequest("rejected")

        publication.status = Publication.Status.ACCEPTED
        publication.updated_by = user.id

        db.session.add(publication)
        db.session.commit()

        self.__notify_publication(publication, user)

        return PublicationSerializer.to_dict(publication)

    def delete(self, id, updated_by):
        publication = Publication.query.filter(
            Publication.id == id,
            Publication.status != Publication.Status.DELETED).first()

        if not publication:
            raise NotFound()

        if publication.status != Publication.Status.PENDING:
            raise BadRequest(message="")

        publication.status = Publication.Status.DELETED
        publication.updated_by = updated_by.id

        db.session.add(publication)
        db.session.commit()

    def update(self, id, data, user):
        mapped_data = self.__map_update_data(data)
        mapped_data['updated_by'] = user.id
        mapped_data['status'] = Publication.Status.PENDING

        publication = Publication.query.filter(
            Publication.id == id,
            Publication.status != Publication.Status.DELETED).first()

        if publication is None:
            raise NotFound()

        if publication.status == Publication.Status.ACCEPTED:
            raise BadRequest("can't edit")

        Publication.query.filter_by(id=id).update(mapped_data)

        self.__remove_publication_tags(publication)
        self.__remove_publication_social_networks(publication)

        publication.social_networks = self.__create_social_networks(data)
        publication.tags = self.__create_tags(data)

        db.session.add(publication)
        db.session.commit()

        self.__add_subcategory(
            company_id=mapped_data['company_id'],
            category=mapped_data['category'],
            subcategory=mapped_data['subcategory'])

        self.__notify_publication(publication, user)

        return PublicationSerializer.to_dict(publication)

    def link(self, id, data, user):
        if 'link' not in data:
            raise BadRequest(message='bad request')

        publication = Publication.query.filter(
            Publication.id == id,
            Publication.status != Publication.Status.DELETED).first()

        if not publication:
            raise NotFound()

        if publication.status is not Publication.Status.ACCEPTED:
            raise BadRequest(message='not accepted')

        publication.link = data['link']

        db.session.commit()

        return PublicationSerializer.to_dict(publication)

    def clone(self, id, data, user):
        publication = Publication.query.filter(
            Publication.id == id,
            Publication.status == Publication.Status.ACCEPTED).first()

        if not publication:
            raise NotFound()

        if data['duration'] == "REPETITIONS":
            return PublicationSerializer.to_array(
                self.__clone_repetitions(publication, data, user))
        if data['duration'] == "UNTIL":
            return PublicationSerializer.to_array(
                self.__clone_until(publication, data, user))

        raise BadRequest(message='invalid duration')

    def __clone_until(self, publication, data, user):
        publications = []

        next_datetime = self.__calculate_next_datetime(
            publication.datetime, data)

        while(next_datetime):
            publications.append(
                self.__create_next_publication(
                    publication, next_datetime, user))

            if next_datetime > self.__convert_to_datetime(data["until"]):
                return publications

            next_datetime = self.__calculate_next_datetime(next_datetime, data)

    def __convert_to_datetime(self, date_time):
        return datetime.datetime.strptime(date_time, "%Y-%m-%d")

    def __calculate_next_datetime(self, actual_date, data):
        periodicity = data['periodicity']

        if periodicity == "DAILY":
            return self.__get_next_daily_date(actual_date)
        if periodicity == "WEEKLY":
            return self.__get_next_weekly_date(actual_date)
        if periodicity == "MONTHLY":
            return self.__get_next_monthly_date(actual_date)

        raise BadRequest(message="invalid periodicity")

    def __create_next_publication(self, publication, next_datetime, user):
        new_publication = Publication(
            company_id=publication.company_id,
            datetime=next_datetime,
            title=publication.title,
            message=publication.message,
            additional=publication.additional,
            image_url=publication.image_url,
            status=publication.status,
            social_networks=self.__clone_social_network(publication),
            tags=self.__clone_tags(publication),
            created_by=user.id,
            parent_id=publication.id
        )

        db.session.add(new_publication)
        db.session.commit()

        return new_publication

    def __clone_repetitions(self, publication, data, user):
        publications = []

        for repetition in range(0, int(data['repetitions'])):
            publications.append(
                self.__clone_repetition(publication, data, repetition, user))

        return publications

    def __clone_repetition(self, publication, data, repetition, user):
        new_publication = Publication(
            company_id=publication.company_id,
            datetime=self.__get_clone_date(
                publication.datetime, data, int(repetition)),
            title=publication.title,
            message=publication.message,
            additional=publication.additional,
            image_url=publication.image_url,
            status=publication.status,
            social_networks=self.__clone_social_network(publication),
            tags=self.__clone_tags(publication),
            created_by=user.id,
            parent_id=publication.id
        )

        db.session.add(new_publication)
        db.session.commit()

        return new_publication

    def __get_clone_date(self, datetime, data, repetition):
        periodicity = data['periodicity']

        if periodicity == "DAILY":
            return self.__get_next_daily_date(datetime, repetition)
        if periodicity == "WEEKLY":
            return self.__get_next_weekly_date(datetime, repetition)
        if periodicity == "MONTHLY":
            return self.__get_next_monthly_date(datetime, repetition)

        raise BadRequest(message="invalid periodicity")

    def __get_next_daily_date(self, date_time, repetition=0):
        return date_time + datetime.timedelta(days=(repetition + 1))

    def __get_next_weekly_date(self, date_time, repetition=0):
        return date_time + datetime.timedelta(days=(7 * (repetition + 1)))

    def __clone_social_network(self, publication):
        return list(
            map(
                lambda network: PublicationSocialNetwork(
                    social_network=network.social_network),
                publication.social_networks))

    def __clone_tags(self, publication):
        return list(
            map(lambda tag: PublicationTag(name=tag.name), publication.tags))

    def __notify_publication(self, publication, user):
        service = NotificationsServiceFactory.get_instance()
        event = "PUBLICATION"
        hashes = self.__get_notification_hashes(publication, user)
        message = PublicationSerializer.to_dict(publication)
        service.send(event, hashes, message)

    def __get_notification_hashes(self, publication, user):
        companies_service = CompaniesServiceFactory.get_instance()
        _, company_users = companies_service.get_company_users(
            publication.company_id)

        hashes = []

        for hash in self.__get_users_hashes(company_users):
            # if hash != user.hash:
            hashes.append(hash)

        return hashes

    def __get_user_companies_ids(self):
        companies_service = CompaniesServiceFactory.get_instance()
        _, user_companies = companies_service.get_user_companies()

        return self.__get_companies_ids(user_companies)

    def __get_companies_ids(self, companies):
        return list(map(lambda company: company['id'], companies))

    def __get_users_hashes(self, users):
        return list(map(lambda user: user['hash'], users))

    def __map_data(self, data):
        mapped_data = {}

        mapped_data['title'] = data['title']
        mapped_data['created_by'] = data['created_by']
        mapped_data['company_id'] = data['company_id']
        mapped_data['datetime'] = "{} {}".format(data['date'], data['time'])
        mapped_data['message'] = data['message']
        mapped_data['additional'] = data['additional']
        mapped_data['image_url'] = self.__upload_image(data['image'])
        mapped_data['category'] = data['category']
        mapped_data['subcategory'] = data['subcategory']

        return mapped_data

    def __map_update_data(self, data):
        mapped_data = {}

        mapped_data['title'] = data['title']
        mapped_data['updated_by'] = data['updated_by']
        mapped_data['company_id'] = data['company_id']
        mapped_data['datetime'] = "{} {}".format(data['date'], data['time'])
        mapped_data['message'] = data['message']
        if 'image' in data and data['image'] is not None:
            mapped_data['image_url'] = self.__upload_image(data['image'])
        mapped_data['category'] = data['category']
        mapped_data['subcategory'] = data['subcategory']

        return mapped_data

    def __upload_image(self, image):
        return S3Uploader().upload(image)

    def __remove_publication_social_networks(self, publication):
        PublicationSocialNetwork.query.filter_by(
            publication_id=publication.id).delete()

    def __remove_publication_tags(self, publication):
        PublicationTag.query.filter_by(
            publication_id=publication.id).delete()

    def __create_tags(self, data):
        if 'tags' not in data or data['tags'] is None:
            return []

        tags = []

        for tag in data['tags'].split(","):
            if tag.strip() != "":
                tags.append(PublicationTag(name=tag))

        return tags

    def __create_social_networks(self, data):
        return list(map(
            lambda network: PublicationSocialNetwork(
                social_network=network), data['social_networks']))

    def __add_subcategory(self, company_id, category, subcategory):
        founded_category = db.session.query(Category).\
            filter(Category.name == category).\
            first()

        founded_subcategory = db.session.query(Category).\
            join(Category.subcategories).\
            filter(Category.id == founded_category.id).\
            filter(Subcategory.company_id == company_id).\
            filter(func.lower(Subcategory.name) == func.lower(subcategory)).\
            first()

        if founded_subcategory is None:
            new_subcategory = Subcategory(
                company_id=company_id,
                category=founded_category,
                name=subcategory)

            db.session.add(new_subcategory)
            db.session.commit()


class CategoryLogics:
    def list(self, id):
        categories = db.session.query(Category).\
            outerjoin(Category.subcategories).\
            filter(or_(
                Subcategory.company_id == id,
                Subcategory.company_id.is_(None))).\
            order_by(Category.id.asc())

        return CategorySerializer.to_array(categories)
