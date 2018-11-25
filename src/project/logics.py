import json
import requests
from sqlalchemy.sql import func

from project import db
from project.models import FacebookAuth
from flask import current_app


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
