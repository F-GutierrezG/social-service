import json
import requests

from flask import current_app
from sqlalchemy.sql import func

from project import db
from project.models import FacebookAuth, Publication, PublicationSocialNetwork
from project.serializers import PublicationSerializer


class PublicationLogics:
    def list(self):
        publications = Publication.query.all()

        return PublicationSerializer.to_array(publications)

    def create(self, data):
        mapped_data = self.__map_data(data)

        publication = Publication(**mapped_data)
        self.__add_publication_social_networks(publication, data)

        db.session.add(publication)
        db.session.commit()

        return PublicationSerializer.to_dict(publication)

    def __map_data(self, data):
        mapped_data = {}

        mapped_data['created_by'] = data['created_by']
        mapped_data['company_id'] = data['company_id']
        mapped_data['datetime'] = "{} {}".format(data['date'], data['time'])
        mapped_data['message'] = data['message']
        mapped_data['image_url'] = self.__upload_image(data['image'])

        return mapped_data

    def __upload_image(self, image):
        return "http://url_falsa"

    def __add_publication_social_networks(self, publication, data):
        for social_network in data['social_networks']:
            publication.social_networks.append(PublicationSocialNetwork(
                social_network=social_network))


class FacebookLogics:
    def oauth(self, user, company_id):
        base_url = current_app.config['FACEBOOK_OAUTH_URL']
        client_id = current_app.config['FACEBOOK_CLIENT_ID']
        redirect_uri = current_app.config['FACEBOOK_REDIRECT_URI']
        state = company_id

        url = '{}?client_id={}&redirect_uri={}&state={}'.format(
            base_url, client_id, redirect_uri, state)

        auth = FacebookAuth.query.filter_by(company_id=company_id).first()
        if auth is None:
            auth = FacebookAuth(company_id=company_id, created_by=user.id)
            db.session.add(auth)
            db.session.commit()

        return url

    def access_token(self, code, company_id):
        base_url = current_app.config['FACEBOOK_ACCESS_TOKEN_URL']
        client_id = current_app.config['FACEBOOK_CLIENT_ID']
        redirect_uri = current_app.config['FACEBOOK_REDIRECT_URI']
        client_secret = current_app.config['FACEBOOK_CLIENT_SECRET']

        auth = FacebookAuth.query.filter_by(company_id=company_id).first()
        auth.code = code
        auth.code_created = func.now()
        db.session.add(auth)
        db.session.commit()

        url = '{}?client_id={}&redirect_uri={}&client_secret={}&code={}'\
            .format(base_url, client_id, redirect_uri, client_secret, code)

        response = requests.get(url)
        data = json.loads(response.text)

        auth.short_lived_access_token = data['access_token']
        auth.short_lived_access_token_created = func.now()

        db.session.add(auth)
        db.session.commit()

        return response, data
