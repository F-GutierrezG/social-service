from companies_service.factories import CompaniesServiceFactory

from project import db
from project.models import Publication, PublicationSocialNetwork
from project.serializers import PublicationSerializer
from project.uploaders import S3Uploader


class NotFound(Exception):
    pass


class BadRequest(Exception):
    def __init__(self, message):
        self.message = message


class PublicationLogics:
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

    def create(self, data):
        mapped_data = self.__map_data(data)

        publication = Publication(**mapped_data)
        self.__add_publication_social_networks(publication, data)

        db.session.add(publication)
        db.session.commit()

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

    def __get_user_companies_ids(self):
        companies_service = CompaniesServiceFactory.get_instance()
        user_companies = companies_service.get_user_companies()

        return self.__get_companies_ids(user_companies)

    def __get_companies_ids(self, companies):
        return list(map(lambda company: company['id'], companies))

    def __map_data(self, data):
        mapped_data = {}

        mapped_data['title'] = data['title']
        mapped_data['created_by'] = data['created_by']
        mapped_data['company_id'] = data['company_id']
        mapped_data['datetime'] = "{} {}".format(data['date'], data['time'])
        mapped_data['message'] = data['message']
        mapped_data['additional'] = data['additional']
        mapped_data['image_url'] = self.__upload_image(data['image'])

        return mapped_data

    def __upload_image(self, image):
        return S3Uploader().upload(image)

    def __add_publication_social_networks(self, publication, data):
        for social_network in data['social_networks']:
            publication.social_networks.append(PublicationSocialNetwork(
                social_network=social_network))
